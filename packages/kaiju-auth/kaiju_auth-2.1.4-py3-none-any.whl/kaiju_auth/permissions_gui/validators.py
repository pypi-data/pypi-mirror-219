# from kaiju_model.model import ValidationError
#
#
# async def match_password_validator(app, key: str, value, ref, **__):
#     if ref["password_confirm"] != ref["password"]:
#         raise ValidationError(f"passwords don't match",
#                               data=dict(key=key, value=value, code='auth.user.mismatch_password'))
#
#
# async def group_exists(app, key: str, value, ref, **__):
#     if type(value) is str:
#         value = [value]
#
#     data = await app.services.groups_gui._group_service.list(
#         conditions={
#             "id": [str(v) for v in value]
#         })
#
#     if not data["count"]:
#         raise ValidationError(f"Not found",
#                               data=dict(key=key, value=value, code='ValidationError.not_exist'))
#
#
# async def group_not_exists(app, key: str, value, ref, **__):
#     if type(value) is str:
#         value = [value]
#
#     data = await app.services.groups_gui._group_service.list(
#         conditions={
#             "id": [str(v) for v in value]
#         })
#
#     if data["count"]:
#         raise ValidationError(f"Is exists",
#                               data=dict(key=key, value=value, code='ValidationError.is_exist'))
