import uuid
from datetime import datetime
from time import time
from typing import cast, Generator

import pytest  # noqa: pytest
import pytest_asyncio

from kaiju_db.tests.test_db import TestSQLService

from kaiju_auth.services import *

__all__ = ['TestPermissionsService', 'TestGroupsService', 'TestUserService', 'TestSessionStore', 'TestKeystore']


@pytest.mark.docker
@pytest.mark.asyncio
class TestPermissionsService(TestSQLService):
    """Test permissions service."""

    table_names = [PermissionService.table.name]

    @staticmethod
    def get_rows(num: int) -> Generator[dict, None, None]:
        for n in range(num):
            yield Permission(id=uuid.uuid4().hex, enabled=True, tag='pytest', description='pytest permission')

    @pytest.fixture
    def _service(self, permission_service):
        return permission_service


@pytest.mark.docker
@pytest.mark.asyncio
class TestGroupsService(TestSQLService):
    """Test permissions service."""

    table_names = [GroupService.group_permissions_table.name, GroupService.table.name, PermissionService.table.name]

    @staticmethod
    def get_rows(num: int) -> Generator[dict, None, None]:
        for n in range(num):
            yield Group(id=uuid.uuid4().hex, tag='pytest', description='pytest group')

    @pytest.fixture
    def _service(self, group_service):
        return group_service

    @staticmethod
    def update_value() -> dict:
        return {'tag': 'pytest2'}

    @staticmethod
    def update_condition() -> dict:
        return {'tag': 'pytest'}

    @staticmethod
    def check_update(row: dict) -> bool:
        return row['tag'] == 'pytest2'

    async def test_group_permission_management(self, _row, _store, permission_service):
        row_id = self.get_pkey(_row)
        _store = cast(GroupService, _store)
        await _store.create(_row)
        permissions = await _store.get_permissions(row_id)
        assert not permissions
        permission = next(TestPermissionsService.get_rows(1))
        await permission_service.create(permission)
        await _store.set_permissions(row_id, [permission['id']])
        permissions = await _store.get_permissions(row_id)
        assert permission['id'] in permissions
        await _store.modify_permissions(row_id, {permission['id']: False})
        permissions = await _store.get_permissions(row_id)
        assert permission['id'] not in permissions


@pytest.mark.docker
@pytest.mark.asyncio
class TestUserService(TestSQLService):
    """Test permissions service."""

    table_names = [
        UserService.user_groups_table.name,
        UserService.table.name,
        GroupService.group_permissions_table.name,
        GroupService.table.name,
        PermissionService.table.name,
    ]

    @staticmethod
    def get_rows(num: int) -> Generator[dict, None, None]:
        for n in range(num):
            _id = uuid.uuid4()
            yield User(
                id=_id,
                username=_id.hex,
                email=f'{_id.hex}@mail.ru',
                full_name='Pytest User',
                password=b'password',
                salt=b'salt',
                is_active=True,
                is_blocked=False,
                settings={},
                created=datetime.now(),
            )

    @pytest.fixture
    def _service(self, user_service):
        user_service.select_columns = {col.name for col in user_service.table.columns}
        return user_service

    def update_value(self):
        return {'is_active': False}

    def check_update(self, row):
        return row['is_active'] is False

    def update_condition(self):
        return {'is_active': True}

    async def test_user_permission_management(self, _row, _store, group_service, permission_service):
        row_id = self.get_pkey(_row)
        _store = cast(UserService, _store)
        await _store.create(_row)
        perm = next(TestPermissionsService.get_rows(1))
        await permission_service.create(perm)
        group = next(TestGroupsService.get_rows(1))
        await group_service.create(group)
        await group_service.set_permissions(group['id'], [perm['id']])
        await _store.set_user_groups(row_id, [group['id']])
        groups = await _store.get_user_groups(row_id)
        assert group['id'] in groups['groups']
        permissions = await _store.get_user_permissions(row_id)
        assert perm['id'] in permissions['permissions']
        await _store.modify_user_groups(row_id, {group['id']: False})
        permissions = await _store.get_user_permissions(row_id)
        assert perm['id'] not in permissions['permissions']

    async def test_authentication(self, _row, _store):
        _store = cast(UserService, _store)
        password = 'Password123#'
        user = await _store.register(username=_row['username'], email=_row['email'], password=password)
        authenticated = await _store.auth(username=_row['username'], password=password)
        assert authenticated['id'] == user['id']
        wrong = await _store.auth(username='wrong', password=password)
        assert not wrong
        wrong = await _store.auth(username=_row['username'], password='wrong')
        assert not wrong
        await _store.change_password(username=_row['username'], password=password, new_password='Password123#new')
        authenticated = await _store.auth(username=_row['username'], password='Password123#new')
        assert authenticated['id'] == user['id']


@pytest.mark.docker
@pytest.mark.asyncio
class TestSessionStore(TestSQLService):
    """Test session storage."""

    @staticmethod
    def get_rows(num: int) -> Generator[dict, None, None]:
        for n in range(num):
            yield Session(
                id=uuid.uuid4().hex,
                user_id=uuid.uuid4(),
                created=datetime.now(),
                data={},
                expires=int(time()) + 1000,
                h_agent=None,
                permissions=frozenset(),
                _changed=True,
                _stored=True,
                _loaded=False,
            ).repr()

    @pytest.fixture
    def _service(self, session_store):
        return session_store

    def update_value(self):
        return {'h_agent': b'bytes'}

    def check_update(self, row):
        return row['h_agent'] == b'bytes'

    def update_condition(self):
        return {'h_agent': None}


@pytest.mark.asyncio
class TestKeystore:
    """Test keystore service."""

    @pytest_asyncio.fixture
    async def _store(self, app, keystore) -> KeystoreService:
        async with app.services:
            yield keystore

    async def test_key_initialization(self, _store, mock_cache):
        kid, key = _store.encryption_key
        assert kid and key
        assert await _store.get_public_key(kid) == await _store.get_public_key()
        assert await mock_cache.exists(_store.ns.get_key(kid))

    async def test_key_gen_task(self, _store, mock_cache):
        kid, _ = _store.encryption_key
        await _store._generate_encryption_key()
        new_kid, _ = _store.encryption_key
        assert kid != new_kid
        assert await mock_cache.exists(_store.ns.get_key(new_kid))


@pytest.mark.asyncio
class TestJWTService:
    @pytest.fixture
    def _claims(self):
        return JWTService.TokenClaims(id=uuid.uuid4(), permissions=frozenset({'pytest'}))

    @pytest_asyncio.fixture
    async def _service(self, app, jwt_service) -> JWTService:
        async with app.services:
            yield jwt_service

    async def test_jwt(self, _service, _claims):
        tokens = await _service.get(_claims)
        tokens = await _service.refresh(tokens['refresh'])
        claims = await _service.auth(tokens['access'])
        assert str(claims['id']) == str(_claims['id'])
        assert list(claims['permissions']) == list(_claims['permissions'])

    async def test_invalid_jwt(self, _service):
        assert not await _service.auth('wrong')
        assert not await _service.refresh('wrong')
