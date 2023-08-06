# import abc
#
# from kaiju_model.fields import StringField, BooleanField, PasswordField, MultiselectField
# from kaiju_model.model import BaseModel
#
# from kaiju_auth.permissions_gui.validators import *
#
# all = (
#     'GroupEditModel',
#     'GroupsViewModel',
#     'UsersViewModel',
#     'UserEditModel',
#     'UserChangePasswordViewModel',
#     'UserChangePasswordModel',
#     'UserCreateModel',
#     'UserChangePasswordAdminViewModel',
#     'AdminChangePasswordModel'
# )
#
#
# class UsersViewModel(BaseModel, abc.ABC):
#     id = StringField()
#     username = StringField()
#     full_name = StringField()
#     is_active = BooleanField()
#     is_blocked = BooleanField()
#
#
# class UserCreateModel(BaseModel, abc.ABC):
#     username = StringField(required=True)
#     full_name = StringField(required=True)
#     email = StringField(required=True)
#     password = PasswordField(new_password=True, required=True)
#     password_confirm = PasswordField(new_password=True, required=True,
#                                      field_validator=match_password_validator)
#
#
# class UserEditModel(BaseModel, abc.ABC):
#     id = StringField(is_system=True)
#     username = StringField(read_only=True)
#     full_name = StringField(required=False)
#     email = StringField(required=False)
#
#
# class UserChangePasswordViewModel(BaseModel, abc.ABC):
#     old_password = PasswordField()
#     password = PasswordField(new_password=True)
#     password_confirm = PasswordField(new_password=False)
#
# class UserChangePasswordAdminViewModel(BaseModel, abc.ABC):
#     password = PasswordField(new_password=True)
#     password_confirm = PasswordField(new_password=False)
#
#
# class UserChangePasswordModel(BaseModel, abc.ABC):
#     old_password = PasswordField(required=True)
#     password = PasswordField(new_password=True, required=True)
#     password_confirm = PasswordField(
#         new_password=True,
#         required=True,
#         field_validator=match_password_validator
#     )
#
# class AdminChangePasswordModel(BaseModel, abc.ABC):
#     password = PasswordField(new_password=True, required=True)
#     password_confirm = PasswordField(
#         new_password=True,
#         required=True,
#         field_validator=match_password_validator
#     )
#
#
# class UserGroupsModel(BaseModel, abc.ABC):
#     groups = MultiselectField(required=True,
#                               options_handler="groups_gui.load")
#
#
# class UserGroupsUpdateModel(BaseModel, abc.ABC):
#     groups = MultiselectField(required=True,
#                               field_validator=group_exists,
#                               options_handler="groups_gui.load")
#
#
# class UserStatusUpdateModel(BaseModel, abc.ABC):
#     is_blocked = BooleanField()
#     is_active = BooleanField()
#
#
# class GroupsViewModel(BaseModel, abc.ABC):
#     id = StringField()
#     description = StringField()
#     tag = StringField()
#
#
# class GroupEditModel(BaseModel, abc.ABC):
#     id = StringField(field_validator=group_exists, read_only=True)
#     description = StringField()
#
#
# class GroupCreateModel(BaseModel, abc.ABC):
#     id = StringField(field_validator=group_not_exists)
#     description = StringField()
