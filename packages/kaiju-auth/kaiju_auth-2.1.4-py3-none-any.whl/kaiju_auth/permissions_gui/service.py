# """
# Methods for groups, users and permission gui
# """
#
# from typing import Union
# from uuid import UUID
#
# import sqlalchemy as sa
# from kaiju_db.services import SQLService, DatabaseService
# from kaiju_model.grid.constructor import GridConstructor
# from kaiju_model.model import ModelValidationException
# from kaiju_tools.exceptions import NotFound, ValidationError, NotAuthorized, PermissionDenied
# from kaiju_tools.rpc.abc import AbstractRPCCompatible
# from kaiju_tools.services import Contextable
#
# from kaiju_auth.models import groups, users
# from kaiju_auth.permissions_gui.models import (
#     GroupsViewModel, GroupEditModel,
#     GroupCreateModel, UserCreateModel,
#     UsersViewModel, UserEditModel,
#     UserChangePasswordModel, UserChangePasswordViewModel,
#     UserGroupsModel, UserGroupsUpdateModel, UserStatusUpdateModel, UserChangePasswordAdminViewModel,
#     AdminChangePasswordModel
# )
# from kaiju_auth.services import *
#
# __all__ = ('UserGUIService', 'GroupGUIService')
#
#
# class UserGUIService(SQLService, Contextable, AbstractRPCCompatible):
#     fields = ["username", "full_name", "is_blocked", "is_active"]
#     service_name = "users_gui"
#     table = users
#     db_service_class = DatabaseService
#     user_service_class = UserService
#     group_service_class = GroupService
#
#     def __init__(self, *args, user_service: Union[str, UserService] = None,
#                  group_service: Union[str, GroupService] = None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._user_service: UserService = user_service
#         self._group_service: GroupService = group_service
#         self.user_groups_table = None
#
#     async def init(self):
#         self._user_service = self.discover_service(self._user_service, cls=self.user_service_class)
#         self.user_groups_table = self._user_service.user_groups_table
#         self._group_service = self.discover_service(self._group_service, cls=self.group_service_class)
#
#     @property
#     def routes(self) -> dict:
#         return {
#             "grid": self.grid,
#             "load": self.load,
#             "get": self.get_user,
#             "create_model": self.get_create_model,
#             "create_user": self.create_user,
#             "password_model": self.get_password_model,
#             "groups_model": self.get_user_groups_model,
#             "update_groups": self.update_user_groups,
#             "change_password": self.change_user_password,
#             "update_status": self.set_user_status,
#             "update_info": self.update_user_info,
#             "status_model": self.get_user_status_model,
#             "modify_group_users": self.update_group_users
#         }
#
#     @property
#     def permissions(self):
#         return {
#             self.DEFAULT_PERMISSION: self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION,
#             "load": self.PermissionKeys.GLOBAL_USER_PERMISSION,
#             "password_model": self.PermissionKeys.GLOBAL_USER_PERMISSION,
#             "change_password": self.PermissionKeys.GLOBAL_USER_PERMISSION,
#             "update_info": self.PermissionKeys.GLOBAL_USER_PERMISSION,
#             "get": self.PermissionKeys.GLOBAL_USER_PERMISSION
#         }
#
#     async def _get_user(self, session, id):
#         conditions = {}
#
#         if type(id) is UUID:
#             conditions["id"] = str(id)
#         else:
#             conditions["username"] = id
#
#         data = await self.list(
#             conditions=conditions
#         )
#         if not data["count"]:
#             raise NotFound
#
#         current_user_id = session["user_id"]
#         permissions = session.get("permissions", set())
#
#         user = data["data"][0]
#
#         if current_user_id != user["id"]:
#             if self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION not in permissions:
#                 raise PermissionDenied(code="message.403")
#
#         return user
#
#     async def get_user(self, session, id=None):
#
#         user = await self._get_user(session, id)
#
#         async with UserEditModel(self.app, init=False, **user) as obj:
#             result = obj.fields
#             return result
#
#     async def get_password_model(self, session, **__):
#         if self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION in session["permissions"]:
#             model = UserChangePasswordAdminViewModel
#         else:
#             model = UserChangePasswordViewModel
#         async with model(self.app, init=False) as obj:
#             result = obj.fields
#             return result
#
#     async def get_user_groups_model(self, session, id, **__):
#         user = await self._get_user(session, id)
#         data = await self._user_service.get_user_groups(user["id"])
#
#         async with UserGroupsModel(self.app, groups=data["groups"], init=False) as obj:
#             result = obj.fields
#             return result
#
#     async def get_create_model(self, **__):
#         async with UserCreateModel(self.app, init=False) as obj:
#             result = obj.fields
#             return result
#
#     async def change_user_password(self, session, id, old_password=None, password=None, password_confirm=None):
#         user = await self._get_user(session, id)
#         username = user["username"]
#
#         if self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION in session["permissions"]:
#             model = AdminChangePasswordModel
#         else:
#             model = UserChangePasswordModel
#
#         async with model(self.app, old_password=old_password,
#                          password=password,
#                          password_confirm=password_confirm):
#             if old_password == password:
#                 raise ValidationError(
#                     'Old password matches the new one.',
#                     code=self.ErrorCodes.USER_IDENTICAL_PASSWORDS_SUPPLIED)
#
#             if self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION not in session["permissions"]:
#                 try:
#                     user = await self._user_service.auth(username=username, password=old_password)
#                     new_password = self._user_service.validate_password(password)
#                 except NotAuthorized:
#                     raise ModelValidationException(fields={"old_password": [{"code": 'auth.user.wrong_password'}]})
#                 except ValidationError as error:
#                     raise ModelValidationException(fields={error.data["key"]: [error.data]})
#
#             try:
#                 new_password = self._user_service.validate_password(password)
#             except ValidationError as error:
#                 raise ModelValidationException(fields={error.data["key"]: [error.data]})
#
#             await self._user_service.set_password(user["id"], user['username'], new_password)
#             return True
#
#     async def update_user_info(self, session, id, **kwargs):
#         user = await self._get_user(session, id)
#
#         if not kwargs:
#             return {
#                 "updated": False
#             }
#
#         async with UserEditModel(self.app, **kwargs) as _:
#             if "email" in kwargs:
#                 self._user_service.validate_email(kwargs["email"])
#
#             try:
#                 await self._user_service.update(
#                     id=user["id"],
#                     data=kwargs
#                 )
#             except ValidationError as error:
#                 raise ModelValidationException(fields={error.data["key"]: [error.data]})
#
#             return {
#                 "updated": True
#             }
#
#     async def load(self, id=None, page=None, per_page=None, query=None, **_):
#         if page is None:
#             page = 1
#
#         if per_page is None:
#             per_page = 24
#
#         result = await self.grid(id=id, page=page, per_page=per_page, query=query)
#         data = []
#
#         for i in result["data"]:
#             _id = list(i.values())[0]["id"]
#             data.append({
#                 "id": _id,
#                 "label": i.get("full_name", {}).get("value", f"[{_id}]") or f"[{_id}]",
#             })
#
#         return {
#             "count": result["count"],
#             "pagination": result["pagination"],
#             "data": data
#         }
#
#     async def _get_group_users(self, id):
#         sql = sa.select([self.user_groups_table.c.user_id]).where(
#             self.user_groups_table.c.group_id == str(id)
#         )
#
#         users = await self._db.fetch(sql)
#         return [str(i["user_id"]) for i in users]
#
#     async def grid(self, page=1, per_page=24, group=None, query=None, **_):
#         conditions = {}
#
#         offset = (page - 1) * per_page
#
#         if group:
#             ids = await self._get_group_users(str(group))
#             if ids:
#                 conditions["id"] = ids
#
#         if query:
#             conditions = [
#                 {
#                     "username": {"~": query},
#                     **conditions
#                 },
#                 {
#                     "full_name": {"~": query},
#                     **conditions
#                 }
#             ]
#
#         data = await self.list(
#             conditions=conditions if conditions else None,
#             offset=offset, limit=per_page)
#
#         count = data["count"]
#         pages = data["pages"]
#
#         models = []
#
#         for i in data["data"]:
#             models.append(UsersViewModel(self.app, **i))
#
#         async with GridConstructor(self.app, models=models, fields=self.fields) as gc:
#             return {
#                 "data": list(gc),
#                 "fields": self.fields,
#                 "pagination": {
#                     "page": page,
#                     "pages": pages,
#                 },
#                 "count": count
#             }
#
#     async def create_user(self, username=None, email=None, full_name=None,
#                           password=None, password_confirm=None):
#
#         async with UserCreateModel(email=email, full_name=full_name, password=password,
#                                    username=username, password_confirm=password_confirm) as _:
#             try:
#
#                 data = await self._user_service.register(
#                     username=username,
#                     email=email,
#                     full_name=full_name,
#                     password=password
#                 )
#             except ValidationError as error:
#                 raise ModelValidationException(fields={error.data["key"]: [error.data]})
#
#             return {
#                 "id": data["id"]
#             }
#
#     async def update_user_groups(self, session, id, groups):
#
#         if not groups:
#             raise ValidationError(code="user_groups.no_groups")
#
#         user = await self._get_user(session, id)
#
#         async with UserGroupsUpdateModel(app=self.app, groups=groups) as _:
#             try:
#                 await self._user_service.set_user_groups(
#                     id=user["id"],
#                     groups={group: True for group in groups}
#                 )
#             except ValidationError as error:
#                 raise ModelValidationException(fields={error.data["key"]: [error.data]})
#
#             return {
#                 "updated": True
#             }
#
#     async def get_user_status_model(self, session, id, **__):
#         user = await self._get_user(session, id)
#
#         async with UserStatusUpdateModel(self.app, init=False, **user) as obj:
#             result = obj.fields
#             return result
#
#     async def set_user_status(self, session, id, **kwargs):
#         data_to_update = {}
#         user = await self._get_user(session, id)
#
#         if "is_active" in kwargs:
#             data_to_update["is_active"] = bool(kwargs["is_active"])
#
#         if "is_blocked" in kwargs:
#             data_to_update["is_blocked"] = bool(kwargs["is_blocked"])
#
#         await self.update(
#             id=user["id"],
#             data=data_to_update
#         )
#
#         return {
#             "updated": True
#         }
#
#     async def update_group_users(self, id, user_id):
#         await self._group_service.get(id)
#
#         if type(user_id) is str:
#             user_id = [user_id]
#
#         for _user_id in user_id:
#             await self.app.services.users.modify_user_groups(id=str(_user_id), groups={id: True})
#
#         return {
#             "updated": True
#         }
#
#
# class GroupGUIService(SQLService, Contextable, AbstractRPCCompatible):
#     service_name = 'groups_gui'
#     table = groups
#     db_service_class = DatabaseService
#     group_service_class = GroupService
#     fields = ["id", "description"]
#
#     def __init__(self, *args, group_service: Union[str, GroupService] = None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._group_service: GroupService = group_service
#
#     async def init(self):
#         self._group_service = self.discover_service(self._group_service, cls=self.group_service_class)
#
#     @property
#     def routes(self):
#         return {
#             "create": self.create,
#             "create_model": self.get_create_model,
#             "grid": self.grid,
#             "load": self.load,
#             "get": self.get_group,
#             "update_info": self.update_info,
#             "update_permissions": self.update_permissions,
#             "load_permissions": self.load_permissions
#         }
#
#     @property
#     def permissions(self):
#         return {
#             self.DEFAULT_PERMISSION: self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION
#         }
#
#     async def get_create_model(self, **__):
#         async with GroupCreateModel(self.app, init=False) as obj:
#             result = obj.fields
#             return result
#
#     async def create(self, id, description=None):
#
#         async with GroupCreateModel(self.app, id=id, description=description) as _:
#             await self._group_service.create(
#                 data={
#                     'id': id,
#                     'description': description
#                 },
#                 columns=None
#             )
#
#             return {
#                 "id": id
#             }
#
#     async def load(self, id=None, page=None, per_page=None, query=None, **_):
#         if page is None:
#             page = 1
#
#         if per_page is None:
#             per_page = 24
#
#         result = await self.grid(id=id, page=page, per_page=per_page, query=query)
#         data = []
#
#         for i in result["data"]:
#             _id = i["id"]["value"]
#             data.append({
#                 "id": _id,
#                 "label": i.get("description", {}).get("value", f"[{_id}]") or f"[{_id}]",
#             })
#
#         return {
#             "pagination": result["pagination"],
#             "data": data
#         }
#
#     async def grid(self, id=None, page=1, query=None, per_page=24, **_):
#         offset = (page - 1) * per_page
#
#         conditions = {}
#
#         if id and type(id) is list:
#             conditions["id"] = [str(id_) for id_ in id]
#         elif id:
#             conditions["id"] = str(id)
#
#         if query:
#             conditions = [
#                 {
#                     "id": {"~": query},
#                     **conditions
#                 },
#                 {
#                     "description": {"~": query},
#                     **conditions
#                 }
#             ]
#
#         data = await self.list(
#             conditions=conditions,
#             offset=offset, limit=per_page)
#
#         count = data["count"]
#         pages = data["pages"]
#
#         models = []
#
#         for i in data["data"]:
#             group = dict(i)
#             models.append(GroupsViewModel(self.app, **group))
#
#         async with GridConstructor(self.app, models=models, fields=self.fields) as gc:
#             return {
#                 "data": list(gc),
#                 "fields": self.fields,
#                 "pagination": {
#                     "page": page,
#                     "pages": pages,
#                 },
#                 "count": count
#             }
#
#     async def get_group(self, id):
#         group = await self._group_service.get(id)
#         async with GroupEditModel(self.app, init=False, id=id, description=group["description"]) as obj:
#             result = obj.fields
#             return result
#
#     async def load_permissions(self, id=None, query=None, **_):
#         await self.get_group(id)
#
#         tags = await self._group_service._permission_service.get_all_permissions(group_by_tag=True, query=query)
#         group_permissions = await self._group_service.get_permissions(id)
#
#         data = []
#         for tag in tags:
#             permissions = [{
#                 "id": permission["id"],
#                 "label": permission["description"] or f"[{permission['id']}]",
#                 "value": permission["id"] in group_permissions
#             } for permission in tag["permissions"]]
#
#             data.append({
#                 "tag": tag["tag"],
#                 "permissions": permissions,
#             })
#
#         return {
#             "data": data,
#             "pagination": {
#                 "page": 1,
#                 "pages": 1
#             }
#         }
#
#     async def update_info(self, id, **kwargs):
#         if not kwargs:
#             return {
#                 "updated": False
#             }
#
#         async with GroupEditModel(self.app, **kwargs) as _:
#             if 'description' in kwargs:
#                 await self._group_service.update(
#                     id=id,
#                     data={
#                         'description': kwargs["description"]
#                     }
#                 )
#
#             return {
#                 "updated": True
#             }
#
#     async def update_permissions(self, id, permissions):
#         await self._group_service.get(id)
#         await self._group_service.modify_permissions(id, permissions=permissions)
#         return {
#             "updated": True
#         }
