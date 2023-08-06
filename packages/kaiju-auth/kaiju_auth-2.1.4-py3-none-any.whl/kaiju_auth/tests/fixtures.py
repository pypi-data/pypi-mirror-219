import pytest  # noqa: pycharm

from kaiju_auth.services import *

__all__ = ['group_service', 'permission_service', 'user_service', 'session_store', 'keystore', 'jwt_service']


@pytest.fixture
def permission_service(app, database_service) -> PermissionService:
    service = PermissionService(app=app, database_service=database_service)
    app.services.add_service(service)
    return service


@pytest.fixture
def group_service(app, database_service, permission_service) -> GroupService:
    service = GroupService(app=app, database_service=database_service, permission_service=permission_service)
    app.services.add_service(service)
    return service


@pytest.fixture
def user_service(app, database_service, group_service) -> UserService:
    service = UserService(app=app, database_service=database_service, group_service=group_service)
    app.services.add_service(service)
    return service


@pytest.fixture
def session_store(app, database_service) -> SessionStore:
    service = SessionStore(app=app, database_service=database_service)
    app.services.add_service(service)
    return service


@pytest.fixture
def keystore(app, mock_cache, scheduler) -> KeystoreService:
    service = KeystoreService(app=app, cache_service=mock_cache, scheduler=scheduler)
    app.services.add_service(service)
    return service


@pytest.fixture
def jwt_service(app, mock_cache, keystore) -> JWTService:
    service = JWTService(app=app, keystore=keystore)
    app.services.add_service(service)
    return service
