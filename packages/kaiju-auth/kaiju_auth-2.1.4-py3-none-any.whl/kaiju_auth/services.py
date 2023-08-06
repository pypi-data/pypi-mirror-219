import asyncio
import random
import re
import uuid
from datetime import datetime
from pathlib import Path
from time import time
from typing import Union, List, FrozenSet, Dict, Optional, Collection, TypedDict

import bcrypt
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_pg
from jwt import decode  # noqa: pycharm
from jwcrypto import jwk, jwt  # noqa: pycharm

import kaiju_tools.jsonschema as j
from kaiju_tools.exceptions import ValidationError, Conflict, NotAuthorized
from kaiju_tools.encoding import load, loads, dumps
from kaiju_tools.interfaces import PublicInterface, UserInterface, Cache, TokenInterface
from kaiju_tools.sessions import TokenClientService
from kaiju_tools.app import ContextableService, SERVICE_CLASS_REGISTRY, Scheduler
from kaiju_db.services import DatabaseService, SQLService
from kaiju_tools.types import Session

__all__ = (
    'PermissionService',
    'GroupService',
    'UserService',
    'User',
    'JWTClientService',
    'SessionStore',
    'UserFixtureService',
    'KeystoreService',
    'JWTService',
    'Permission',
    'Group',
    'Session',
)


class Permission(TypedDict, total=False):
    """Permission object."""

    id: str
    enabled: bool
    tag: str
    description: str


class PermissionService(SQLService[str, Permission], ContextableService, PublicInterface):
    """Service which stores user permission keys and information about them."""

    class _TaggedPermissions(TypedDict):
        tag: Optional[str]
        permissions: List[dict]

    table = sa.Table(
        'permissions',
        sa.MetaData(),
        sa.Column('id', sa.TEXT, primary_key=True, nullable=False),
        sa.Column('enabled', sa.Boolean, nullable=False, default=True),
        sa.Column('tag', sa.TEXT, nullable=True),
        sa.Column('description', sa.TEXT, nullable=True),
    )

    service_name = 'permissions'
    update_columns_blacklist = {'id'}

    @property
    def routes(self) -> dict:
        return {**super().routes, 'get_all': self.get_all_permissions}

    @property
    def validators(self):
        return {**super().validators, 'get_all': j.Object({'group_by_tag': j.Boolean()})}

    async def get_all_permissions(
        self, group_by_tag=True, id=None, query=None
    ) -> Union[List[dict], List[_TaggedPermissions]]:
        """Return all active permissions in alphabetic order.

        :param id:
        :param group_by_tag: permissions will be grouped by a permission tag
        :param query: search by permission tag or description
        """
        conditions = [self.table.c.enabled.is_(True)]

        if query:
            conditions.append(sa.func.lower(self.table.c.description).op('~')(sa.func.lower(query)))
            conditions.append(sa.func.lower(self.table.c.id).op('~')(sa.func.lower(query)))

        if id:
            if type(id) is not list:
                id = [id]

            conditions.append(self.table.c.id.in_(id))

        sql = self.table.select().where(sa.and_(*conditions)).order_by(self.table.c.tag, self.table.c.id)
        data = await self._db.fetch(sql)
        # data = self._filter_columns(data, self.select_columns)
        if group_by_tag:
            result = {}
            for row in data:
                tag = row['tag']
                if tag in result:
                    result[tag].append(row)
                else:
                    result[tag] = [row]
            data = [{'tag': tag, 'permissions': _permissions} for tag, _permissions in result.items()]
        return data


class Group(TypedDict, total=False):
    """User group object."""

    id: str
    tag: str
    description: str


class GroupService(SQLService[str, Group], ContextableService, PublicInterface):
    """User groups and their permissions."""

    class _GroupPermissions(TypedDict):
        id: str
        permissions: FrozenSet[str]

    table = sa.Table(
        'groups',
        sa.MetaData(),
        sa.Column('id', sa.TEXT, primary_key=True, nullable=False),
        sa.Column('tag', sa.TEXT, nullable=True),
        sa.Column('description', sa.TEXT, nullable=True),
    )

    group_permissions_table = sa.Table(
        'group_permissions',
        sa.MetaData(),
        sa.Column('group_id', sa.TEXT, sa.ForeignKey(table.c.id, ondelete='CASCADE'), nullable=False, primary_key=True),
        sa.Column(
            'permission_id',
            sa.TEXT,
            sa.ForeignKey(PermissionService.table.c.id, ondelete='CASCADE'),
            nullable=False,
            primary_key=True,
        ),
    )

    permissions_table = PermissionService.table

    service_name = 'user_groups'
    db_service_class = DatabaseService
    permission_service_class = PermissionService
    update_columns_blacklist = {'id'}

    def __init__(
        self,
        app,
        database_service: DatabaseService = None,
        permission_service: PermissionService = None,
        logger=None,
    ):
        """Initialize.

        :param app: web app
        :param database_service: db service instance or name
        :param permission_service: permissions service instance or name
        :param logger: logger instance
        """
        super().__init__(app=app, database_service=database_service, logger=logger)
        self._db.add_table(self.group_permissions_table)
        self.permissions_table = self.permission_service_class.table
        self._permission_service = permission_service

    @property
    def routes(self) -> dict:
        return {
            **super().routes,
            'permissions.get': self.get_permissions,
            'permissions.set': self.set_permissions,
            'permissions.update': self.modify_permissions,
        }

    async def init(self):
        self._permission_service = self.discover_service(self._permission_service, cls=self.permission_service_class)
        self.permissions_table = self._permission_service.table

    async def get_permissions(self, id: Union[str, Collection[str]]) -> Union[frozenset, List[_GroupPermissions]]:
        """Return group(s) permissions. Non-active permission keys will be ignored.

        :param id: group identifier
        :returns: a set of permissions
        """
        if isinstance(id, Collection) and not type(id) is str:
            if not id:
                return []

            sql = (
                sa.select(*[self.group_permissions_table.c.group_id, self.group_permissions_table.c.permission_id])
                .select_from(
                    self.group_permissions_table.join(
                        self.permissions_table,
                        sa.and_(
                            self.group_permissions_table.c.permission_id == self.permissions_table.c.id,
                        ),
                    )
                )
                .where(
                    sa.and_(self.group_permissions_table.c.group_id.in_(id), self.permissions_table.c.enabled.is_(True))
                )
            )
            rows = await self._db.fetch(sql)
            _groups = {group_id: [] for group_id in id}
            for row in rows:
                _groups[row['group_id']].append(row['permission_id'])
            result = [
                {'id': group_id, 'permissions': frozenset(_permissions)} for group_id, _permissions in _groups.items()
            ]
        else:
            sql = (
                sa.select(*[self.group_permissions_table.c.permission_id])
                .select_from(
                    self.group_permissions_table.join(
                        self.permissions_table,
                        sa.and_(
                            self.group_permissions_table.c.permission_id == self.permissions_table.c.id,
                        ),
                    )
                )
                .where(
                    sa.and_(self.group_permissions_table.c.group_id == id, self.permissions_table.c.enabled.is_(True))
                )
            )
            rows = await self._db.fetch(sql)
            result = frozenset(row['permission_id'] for row in rows)

        return result

    async def set_permissions(self, id: str, permissions: Collection[str]) -> frozenset:
        """Set permissions in the group.

        All non-mentioned permissions will be removed.

        :param id: group identifier
        :param permissions: a list of permissions
        :returns: a new set of available permissions
        """
        _permissions = set(permissions)
        _existing_permissions = await self.get_permissions(id)
        _to_delete = _existing_permissions.difference(_permissions)
        _to_add = _permissions.difference(_existing_permissions)
        tasks = []

        if _to_delete:
            sql = self.group_permissions_table.delete().where(
                sa.and_(
                    self.group_permissions_table.c.permission_id.in_(list(_to_delete)),
                    self.group_permissions_table.c.group_id == id,
                )
            )
            tasks.append(self._db.execute(sql))

        if _to_add:
            sql = self.group_permissions_table.insert().values(
                [{'group_id': id, 'permission_id': key} for key in _to_add]
            )
            tasks.append(self._db.execute(sql))

        await asyncio.gather(*tasks)
        return frozenset(permissions)

    async def modify_permissions(self, id: str, permissions: Dict[str, bool]) -> frozenset:
        """Modify permissions in a group.

        .. code-block:: python

            await groups.modify_permissions('users', {'do.this': True, 'do.that': False})

        :param id: group identifier
        :param permissions: { <permission key>: <bool> } mapping
        :returns: a new set of available permissions
        """
        if not permissions:
            return await self.get_permissions(id)
        keys = list(permissions.keys())
        sql_1 = self.permissions_table.select().where(self.permissions_table.c.id.in_(keys))
        sql_2 = self.group_permissions_table.select().where(
            sa.and_(
                self.group_permissions_table.c.permission_id.in_(keys), self.group_permissions_table.c.group_id == id
            )
        )

        keys, existing_keys, _ = await asyncio.gather(
            self._db.fetch(sql_1), self._db.fetch(sql_2), self.get(id, columns=['id'])
        )

        keys = {row['id'] for row in keys}
        existing_keys = {row['permission_id'] for row in existing_keys}
        to_add, to_remove = [], []

        for permission_key, value in permissions.items():
            if permission_key in keys:
                if value and permission_key not in existing_keys:
                    to_add.append(permission_key)
                else:
                    to_remove.append(permission_key)

        tasks = []

        if to_remove:
            sql_1 = self.group_permissions_table.delete().where(
                sa.and_(
                    self.group_permissions_table.c.permission_id.in_(to_remove),
                    self.group_permissions_table.c.group_id == id,
                )
            )
            tasks.append(self._db.execute(sql_1))
        data = [{'group_id': id, 'permission_id': permission_id} for permission_id in to_add]
        if data:
            sql_2 = self.group_permissions_table.insert().values(data)
            tasks.append(self._db.execute(sql_2))

        await asyncio.gather(*tasks)
        return await self.get_permissions(id)


class User(TypedDict, total=False):
    """User data object."""

    id: uuid.UUID
    username: str
    email: Optional[str]
    full_name: Optional[str]
    password: bytes
    salt: bytes
    is_active: bool
    is_blocked: bool
    settings: dict
    created: datetime


class UserService(SQLService[uuid.UUID, User], ContextableService, PublicInterface, UserInterface):
    """Information about users and user groups."""

    class ErrorCode:
        """User service error codes."""

        RPC_PERMISSION_DENIED = 'auth.rpc.permission_denied'

        USER_NOT_FOUND = 'auth.user.not_found'
        USER_EXISTS = 'auth.user.exists'
        USER_AUTH_FAILED = 'auth.user.authentication_failed'
        USER_IDENTICAL_PASSWORDS_SUPPLIED = 'auth.user.identical_passwords_supplied'
        USER_INVALID_EMAIL = 'auth.user.invalid_email'
        USER_INVALID_USERNAME = 'auth.user.invalid_username'
        USER_WEAK_PASSWORD = 'auth.user.weak_password'
        USER_INVALID_PASSWORD = 'auth.user.invalid_password'

        GROUP_NOT_FOUND = 'auth.group.not_found'
        GROUP_EXISTS = 'auth.group.exists'
        GROUP_CANT_EDIT = 'auth.group.cant_edit'
        GROUP_CANT_DELETE = 'auth.group.cant_delete'
        GROUP_PARENT_NOT_FOUND = 'auth.group.parent_group_not_found'
        GROUP_CANT_INHERIT_ITSELF = 'auth.group.cant_inherit_itself'
        GROUP_CANT_HAVE_PARENT = 'auth.group.cant_have_parent'
        GROUP_PARENT_MUST_BE_SYSTEM = 'auth.group.parent_group_must_be_system_group'

        PERMISSION_NOT_FOUND = 'auth.permission.not_found'
        PERMISSION_EXISTS = 'auth.permission.exists'

    class _UserGroups(TypedDict):
        id: uuid.UUID
        groups: List[str]

    class _UserPermissions(TypedDict):
        id: uuid.UUID
        permissions: FrozenSet[str]

    table = sa.Table(
        'users',
        sa.MetaData(),
        sa.Column('id', sa_pg.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('username', sa.TEXT, unique=True, nullable=False),
        sa.Column('email', sa.TEXT, unique=True, nullable=False),
        sa.Column('full_name', sa.TEXT, nullable=True),
        sa.Column('password', sa_pg.BYTEA, nullable=False),
        sa.Column('salt', sa_pg.BYTEA, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('is_blocked', sa.Boolean, nullable=False, default=False),
        sa.Column('settings', sa_pg.JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column(
            'created',
            sa.DateTime,
            nullable=False,
            default=datetime.utcnow,
            server_default=sa.func.timezone('UTC', sa.func.current_timestamp()),
        ),
    )

    user_groups_table = sa.Table(
        'user_groups',
        sa.MetaData(),
        sa.Column(
            'group_id',
            sa.TEXT,
            sa.ForeignKey(GroupService.table.c.id, ondelete='CASCADE'),
            nullable=False,
            primary_key=True,
        ),
        sa.Column(
            'user_id',
            sa_pg.UUID(as_uuid=True),
            sa.ForeignKey(table.c.id, ondelete='CASCADE'),
            nullable=False,
            primary_key=True,
        ),
    )

    service_name = 'users'

    salt_rounds = 13  #: OWASP recommendation
    bad_password_timeout = 0.5  #: timeout in sec if auth failed
    bad_password_timeout_jitter = 0.5  #: timeout jitter in sec if auth failed

    min_password_len = 12  #: OWASP recommendation
    max_password_len = 128  #: OWASP recommendation
    password_regex = re.compile(rf'^(?=.*\d).{{{min_password_len},{max_password_len}}}$')

    min_username_len = 4
    max_username_len = 32
    username_regex = re.compile(rf'^[\w0-9_-]{{{min_username_len},{max_username_len}}}$')

    email_regex = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

    _username_regex = re.compile(username_regex)
    _password_regex = re.compile(password_regex)
    _email_regex = re.compile(email_regex)

    update_columns_blacklist = {'id'}
    select_columns_blacklist = {'password', 'salt'}

    def __init__(
        self,
        app,
        database_service: DatabaseService = None,
        group_service: GroupService = None,
        default_group: str = None,
        default_nonlogin_group: str = None,
        salt_rounds=salt_rounds,
        min_password_len=min_password_len,
        max_password_len=max_password_len,
        min_username_len=min_username_len,
        max_username_len=max_username_len,
        bad_password_timeout=bad_password_timeout,
        bad_password_timeout_jitter=bad_password_timeout_jitter,
        logger=None,
    ):
        """Initialize.

        :param app: web app
        :param database_service: db service instance or name
        :param group_service: user group service instance or name
        :param default_group: default group to use for new registered users
        :param default_nonlogin_group: default group for guest users
        :param salt_rounds:
        :param min_password_len:
        :param max_password_len:
        :param min_username_len:
        :param max_username_len:
        :param bad_password_timeout: time to wait between failed login attempts
        :param bad_password_timeout_jitter:
        """
        super().__init__(app=app, database_service=database_service, logger=logger)
        self._db.add_table(self.user_groups_table)
        self._default_group = default_group
        self._default_nonlogin_group = default_nonlogin_group
        self.salt_rounds = salt_rounds
        self.bad_password_timeout = bad_password_timeout
        self.bad_password_timeout_jitter = bad_password_timeout_jitter
        self.min_username_len = min_username_len
        self.max_username_len = max_username_len
        self.min_password_len = min_password_len
        self.max_password_len = max_password_len
        self._group_service = group_service

    @property
    def routes(self) -> dict:
        return {
            **super().routes,
            'groups.get': self.get_user_groups,
            'groups.set': self.set_user_groups,
            'groups.update': self.modify_user_groups,
            'permissions.get': self.get_user_permissions,
            'permissions.get_defaults': self.get_default_permissions,
            'permissions.get_nonlogin_defaults': self.get_default_nonlogin_permissions,
        }

    @property
    def permissions(self) -> dict:
        return {'*': self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION}

    async def init(self):
        self._group_service = self.discover_service(self._group_service, cls=GroupService)

    async def get_default_permissions(self) -> frozenset:
        """Return a set of default user group permissions."""
        if self._default_group:
            return await self._group_service.get_permissions(self._default_group)
        else:
            return frozenset()

    async def get_default_nonlogin_permissions(self) -> frozenset:
        """Return a set of guest user permissions."""
        if self._default_nonlogin_group:
            return await self._group_service.get_permissions(self._default_nonlogin_group)
        else:
            return frozenset()

    async def get_user_groups(self, id: uuid.UUID) -> _UserGroups:
        """Return a list of groups of a user."""
        sql = (
            self.user_groups_table.select()
            .with_only_columns(*[self.user_groups_table.c.group_id])
            .where(self.user_groups_table.c.user_id == id)
        )
        rows = await self._db.fetch(sql)
        _groups = list(row['group_id'] for row in rows)
        if not _groups and self._default_group:
            _groups = [self._default_group]
        return {'id': id, 'groups': _groups}

    async def set_user_groups(self, id: uuid.UUID, groups: Collection[str]):
        """Set groups for a user. All non-mentioned groups will be removed."""
        _groups = set(groups)
        _existing_groups = await self.get_user_groups(id)
        _existing_groups = set(_existing_groups['groups'])
        _to_delete = _existing_groups.difference(_groups)
        _to_add = _groups.difference(_existing_groups)
        tasks = []

        if _to_delete:
            sql = self.user_groups_table.delete().where(
                sa.and_(self.user_groups_table.c.user_id == id, self.user_groups_table.c.group_id.in_(list(_to_delete)))
            )
            tasks.append(self._db.execute(sql))

        if _to_add:
            sql = self.user_groups_table.insert().values([{'user_id': id, 'group_id': key} for key in _to_add])
            tasks.append(self._db.execute(sql))

        await asyncio.gather(*tasks)

    async def modify_user_groups(self, id: uuid.UUID, groups: Dict[str, bool]) -> _UserGroups:
        """Modify user groups."""
        if not groups:
            return await self.get_user_groups(id)

        keys = list(groups.keys())
        sql = (
            self.user_groups_table.select()
            .with_only_columns(*[self.user_groups_table.c.group_id])
            .where(sa.and_(self.user_groups_table.c.user_id == id, self.user_groups_table.c.group_id.in_(keys)))
        )
        rows = await self._db.fetch(sql)
        existing_groups = {row['group_id'] for row in rows}
        to_remove, to_add = [], []

        for group_id, value in groups.items():
            if value:
                if group_id not in existing_groups:
                    to_add.append(group_id)
            else:
                if group_id in existing_groups:
                    to_remove.append(group_id)

        tasks = []

        if to_add:
            data = [{'user_id': id, 'group_id': group_id} for group_id in to_add]
            sql = self.user_groups_table.insert().values(data)
            tasks.append(self._db.execute(sql))

        if to_remove:
            sql = self.user_groups_table.delete().where(
                sa.and_(self.user_groups_table.c.user_id == id, self.user_groups_table.c.group_id.in_(to_remove))
            )
            tasks.append(self._db.execute(sql))

        await asyncio.gather(*tasks)
        return await self.get_user_groups(id)

    async def get_user_permissions(self, id: uuid.UUID) -> _UserPermissions:
        """Get user permissions."""
        _groups = await self.get_user_groups(id)
        if _groups:
            _permissions = await self._group_service.get_permissions(_groups['groups'])
            _permissions = set().union(*(_group['permissions'] for _group in _permissions))
            _permissions = frozenset(_permissions)
        else:
            _permissions = frozenset()

        return {'id': id, 'permissions': _permissions}

    async def register(self, username: str, email: str, password: str, settings: dict = None) -> User:
        """Add a new user. Used by administrators or user managers."""
        self.validate_username(username)
        self.validate_email(email)
        password = self.validate_password(password)

        sql = self.table.select().where(sa.or_(self.table.c.username == username, self.table.c.email == email))

        data = await self._db.fetchrow(sql)

        if data is not None:
            raise Conflict(
                'User or e-mail address is already registered.', key=username, code=self.ErrorCode.USER_EXISTS
            )

        salt, password = self._hash_password(username, password)
        if settings is None:
            settings = {}
        settings['username'] = username
        settings['email'] = email
        settings['password'] = password
        settings['salt'] = salt
        settings['id'] = uuid.uuid4()
        sql = self.table.insert().values(settings)
        await self._db.execute(sql)
        return await self.get_user_and_permissions(settings['id'])

    async def update_profile(self, id: uuid.UUID, settings: dict):
        data = await self.get(id, columns=['settings'])
        meta = data['settings']
        for key, value in settings.items():
            if value is None:
                if key in meta:
                    del meta[key]
            else:
                meta[key] = value
        await self.update(id, {'settings': meta})
        return {'id': id, 'settings': meta}

    async def auth(self, username: str, password: str) -> Optional[User]:
        """Get user authorization."""
        sql = (
            self.table.select()
            .with_only_columns(*[self.table.c.id, self.table.c.password, self.table.c.salt])
            .where(
                sa.and_(
                    self.table.c.username == username,
                    self.table.c.is_active.is_(True),
                    self.table.c.is_blocked.is_(False),
                )
            )
        )
        user = await self._db.fetchrow(sql)

        if user is None:
            return
            # raise NotAuthorized('User authentication failed.', code=self.ErrorCode.USER_AUTH_FAILED)

        if not self._check_password(username, password, user['salt'], user['password']):
            return
            # raise NotAuthorized('User authentication failed.', code=self.ErrorCode.USER_AUTH_FAILED)

        return await self.get_user_and_permissions(user['id'])

    async def change_password(self, username: str, password: str, new_password: str):

        if password == new_password:
            raise ValidationError(
                'Old password matches the new one.', code=self.ErrorCode.USER_IDENTICAL_PASSWORDS_SUPPLIED
            )

        new_password = self.validate_password(new_password)
        user = await self.auth(username=username, password=password)
        await self.set_password(user['id'], username, new_password)
        return True

    async def set_password(self, id: uuid.UUID, username: str, password: str):
        salt, password = self._hash_password(username, password)
        sql = (
            self.table.update()
            .where(sa.and_(self.table.c.id == id, self.table.c.username == username))
            .values(password=password, salt=salt)
        )
        await self._db.execute(sql)

    def validate_email(self, email: str):
        if not self._email_regex.fullmatch(email):
            raise ValidationError(
                'Enter a valid e-mail address.', key='email', value=None, code=self.ErrorCode.USER_INVALID_EMAIL
            )

    def validate_username(self, username: str):
        if not self._username_regex.fullmatch(username):
            raise ValidationError(
                f'Username must be from {self.min_username_len} up to'
                f' {self.max_username_len} characters,'
                f' only letters, numbers and _ . - are allowed.',
                key='username',
                value=None,
                min_characters=self.min_username_len,
                max_characters=self.max_username_len,
                code=self.ErrorCode.USER_INVALID_USERNAME,
            )

    def validate_password(self, password: str):
        password = password.strip(' \n\t\r')
        if not self._password_regex.fullmatch(password):
            raise ValidationError(
                f'Password must contain {self.min_password_len} up to'
                f' {self.max_password_len} characters at least one of them'
                f' must be a digit.',
                key='password',
                value=None,
                min_characters=self.min_password_len,
                max_characters=self.max_password_len,
                code=self.ErrorCode.USER_INVALID_PASSWORD,
            )
        return password

    def _hash_password(self, username, password, salt=None) -> (bytes, bytes):
        if salt is None:
            salt = bcrypt.gensalt(self.salt_rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        if not self._check_password(username, password, salt, hashed):
            raise RuntimeError('Internal error.')
        return salt, hashed

    @staticmethod
    def _check_password(username, password, salt, hashed) -> bool:
        result = bcrypt.checkpw(password.encode('utf-8'), hashed)
        return result

    def _get_timeout(self):
        return random.random() * self.bad_password_timeout_jitter + self.bad_password_timeout

    def process_update_data(self, password=None, salt=None, created=None, id=None, **data):
        return data

    async def get_user_and_permissions(self, id) -> dict:
        user = await self.get(id)
        _permissions = await self.get_user_permissions(id)
        return {**user, 'permissions': _permissions['permissions']}


class JWTClientService(TokenClientService):
    """JWT client which renews tokens automatically."""

    def _get_exp_time(self, token: str) -> int:
        data = decode(token, options={'verify_signature': False})
        return data['exp']


class SessionStore(SQLService, PublicInterface):
    """Session data storage."""

    table = sa.Table(
        'sessions',
        sa.MetaData(),
        sa.Column('id', sa.TEXT, primary_key=True),
        sa.Column('h_agent', sa_pg.BYTEA, nullable=True),
        sa.Column('user_id', sa_pg.UUID(as_uuid=True), nullable=True),
        sa.Column('expires', sa.INTEGER, nullable=False),
        sa.Column('permissions', sa_pg.JSONB, nullable=False),
        sa.Column('data', sa_pg.JSONB, nullable=False),
        sa.Column('created', sa.TIMESTAMP, nullable=False),
    )


class KeystoreService(ContextableService):
    """Shared key storage."""

    def __init__(
        self,
        *args,
        cache_service: Cache = None,
        scheduler: Scheduler = None,
        ttl: int = 3600 * 24,
        algorithm: str = 'EC',
        key_size: str = 256,
        shared: bool = True,
        **kws,
    ):
        """Initialize.

        :param cache_service: cache service string or instance
        :param ttl: key lifetime in seconds
        :param algorithm: encryption algorithm
        :param key_size: encryption key size
        :param shared: public keys are shared between different apps
        """
        super().__init__(*args, **kws)
        self.ns = self.app.namespace_shared if shared else self.app.namespace
        self.ns = self.ns / '_kid'
        self._cache = cache_service
        self._scheduler = scheduler
        self.ttl = ttl
        self.algorithm = algorithm
        self.key_size = key_size
        self._kid = None
        self._key = None
        self._pkey = None
        self._deadline = None
        self._task_renew_keys = None

    async def init(self):
        self._cache = self.discover_service(self._cache, cls=Cache)
        self._scheduler = self.discover_service(self._scheduler, cls=Scheduler)
        await self._generate_encryption_key()
        self._task_renew_keys = self._scheduler.schedule_task(
            self._generate_encryption_key,
            interval=self.ttl / 2,
            retries=10,
            name=f'{self.service_name}._generate_encryption_key',
        )

    async def close(self):
        self._task_renew_keys.enabled = False
        # await self._cache.delete(self.ns.get_key(self._kid))

    @property
    def encryption_key(self) -> (str, jwt.JWK):
        """Get a key pair."""
        return self._kid, self._key

    async def get_public_key(self, kid: str = None) -> Optional[jwk.JWK]:
        """Get a public key by its id."""
        if kid is None or kid == self._kid:
            return self._pkey
        pkey = await self._cache.get(self.ns.get_key(kid))
        if pkey:
            return jwk.JWK(**pkey)

    async def _generate_encryption_key(self) -> None:
        """Generate and set a new key pair and key deadline and push the public key to the shared store (cache)."""
        kid = uuid.uuid4().hex
        key = jwk.JWK.generate(kty=self.algorithm, size=self.key_size, kid=kid)
        pkey = key.export_public(as_dict=True)
        self._pkey = jwk.JWK(**pkey)
        self._kid = kid
        self._key = key
        self._deadline = time() + self.ttl
        await self._cache.set(self.ns.get_key(self._kid), pkey, ttl=self.ttl)


class JWTService(ContextableService, TokenInterface):
    """JWT token generation and validation."""

    class _JWT(jwt.JWT):
        """Customized json serializer."""

        @property
        def claims(self):
            if self._claims is None:
                raise KeyError("'claims' not set")
            return self._claims

        @claims.setter
        def claims(self, c):
            if not isinstance(c, dict):
                if not self._reg_claims:
                    # no default_claims, can return immediately
                    self._claims = c
                    return
                c = loads(c)
            else:
                # _add_default_claims modifies its argument
                # so we must always copy it.
                c = c.copy()

            self._add_default_claims(c)
            self._claims = dumps(c)

    def __init__(
        self,
        *args,
        keystore: KeystoreService = None,
        access_token_ttl: int = 1000,
        refresh_token_ttl: int = 3600 * 24,
        algorithm: str = 'ES256',
        **kws,
    ):
        """Initialize.

        :param keystore: keystore service
        :param access_token_ttl: access token lifetime sec
        :param refresh_token_ttl: refresh token lifetime sec
        """
        super().__init__(*args, **kws)
        self.algorithm = algorithm
        self._access_token_ttl = max(60, int(access_token_ttl))
        self._refresh_token_ttl = max(self._access_token_ttl, refresh_token_ttl)
        self._keystore = keystore

    async def init(self):
        self._keystore = self.discover_service(self._keystore, cls=KeystoreService)

    async def auth(self, token: str, /) -> Optional[TokenInterface.TokenClaims]:
        token = await self.load_token(token)
        if token:
            return loads(token.claims)

    async def get(self, claims: TokenInterface.TokenClaims, /) -> TokenInterface.TokenInfo:
        """Get a new JWT token pair."""
        return self._get_token_pair(claims)

    async def refresh(self, token: str, /) -> Optional[TokenInterface.TokenInfo]:
        """Get a refreshed pair of JWT tokens."""
        token = await self.load_token(token)
        if token:
            return self._get_token_pair(loads(token.claims))

    def _get_token_pair(self, claims) -> Optional[TokenInterface.TokenInfo]:
        kid, key = self._keystore.encryption_key
        access = self._generate_token(kid, key, claims, ttl=self._access_token_ttl)
        refresh = self._generate_token(kid, key, claims, ttl=self._refresh_token_ttl)
        return TokenInterface.TokenInfo(access=access.serialize(), refresh=refresh.serialize())

    async def load_token(self, token: str) -> Optional[jwt.JWT]:
        """Load a JWT token.

        :return: a JWT token or nothing if the token is invalid or expired
        """
        try:
            token = self._JWT(jwt=token)
        except (jwt.JWException, KeyError, ValueError):
            return
        kid = token.token.jose_header.get('kid')
        if not kid:
            return
        pkey = await self._keystore.get_public_key(kid)
        if not pkey:
            return
        try:
            token.validate(pkey)
        except (jwt.JWException, KeyError, ValueError):
            raise NotAuthorized('Invalid authorization token.', service=self.service_name)
        return token

    def _generate_token(self, kid: str, key: jwt.JWK, data: dict, ttl: int) -> jwt.JWT:
        iat = int(time())
        exp = int(min(iat + ttl, self._keystore._deadline))
        token = self._JWT(
            header={'typ': 'JWT', 'alg': self.algorithm, 'kid': kid},
            claims={
                **data,
                'iat': iat,
                'exp': exp,
            },
        )
        token.make_signed_token(key)
        return token


class UserFixtureService(ContextableService):
    """Base user fixture service."""

    def __init__(
        self,
        *args,
        permission_service: PermissionService = None,
        group_service: GroupService = None,
        user_service: UserService = None,
        base_dir='./fixtures/users',
        **kws,
    ):
        super().__init__(*args, **kws)
        self._base_dir = Path(base_dir)
        self._permission_service: PermissionService = permission_service
        self._group_service: GroupService = group_service
        self._user_service: UserService = user_service

    async def init(self):
        self._permission_service = self.discover_service(name=self._permission_service, cls=PermissionService)
        self._group_service: GroupService = self.discover_service(name=self._group_service, cls=GroupService)
        self._user_service: UserService = self.discover_service(name=self._user_service, cls=UserService)
        await self.load_user_permissions()
        await self.load_user_groups()
        await self.load_users()

    async def load_user_permissions(self):
        service = self._permission_service
        path = self._base_dir / 'permissions.json'
        self.logger.debug('Loading user permissions from: %s.', path)
        data = self.load_file(path)
        if data:
            keys = [row['id'] for row in data]
            existing = await service.m_exists(keys)
            data = [row for row in data if row['id'] not in existing]
            self.logger.debug('Adding %d new permissions.', len(data))
            if data:
                await service.m_create(data, columns=None)
        else:
            self.logger.debug('No user permission fixtures have been found.')

    async def load_user_groups(self):
        service = self._group_service
        path = self._base_dir / 'groups.json'
        self.logger.debug('Loading user groups from: %s.', path)
        data = self.load_file(path)
        if data:
            for row in data:
                group = row['data']
                _id = group['id']
                group_permissions = row['permissions']
                if not await service.exists(_id):
                    self.logger.debug('Adding new group "%s".', _id)
                    await service.create(group, columns=None)
                if group_permissions:
                    await service.set_permissions(_id, group_permissions)
        else:
            self.logger.debug('No user group fixtures have been found.')

    async def load_users(self):
        service = self._user_service
        path = self._base_dir / 'users.json'
        self.logger.debug('Loading users from: %s.', path)
        data = self.load_file(path)
        if data:
            for row in data:
                user = row['data']
                user_groups = row['groups']
                username = user['username']
                data = await service.list(conditions={'username': username}, columns='id')
                data = data['data']
                if data:
                    user_id = data[0]['id']
                else:
                    self.logger.debug('Adding new user "%s".', username)
                    user = await service.register(**user)
                    user_id = user['id']
                if user_groups:
                    await service.set_user_groups(user_id, user_groups)
        else:
            self.logger.debug('No user fixtures have been found.')

    @staticmethod
    def load_file(path: Path):
        if path.exists():
            with open(path) as f:
                return load(f)


SERVICE_CLASS_REGISTRY.register(PermissionService)
SERVICE_CLASS_REGISTRY.register(GroupService)
SERVICE_CLASS_REGISTRY.register(UserService)
SERVICE_CLASS_REGISTRY.register(JWTClientService)
SERVICE_CLASS_REGISTRY.register(SessionStore)
SERVICE_CLASS_REGISTRY.register(UserFixtureService)
SERVICE_CLASS_REGISTRY.register(KeystoreService)
SERVICE_CLASS_REGISTRY.register(JWTService)
