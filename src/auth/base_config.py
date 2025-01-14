from fastapi import Depends, Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (CookieTransport, AuthenticationBackend,
                                          BearerTransport)
from fastapi_users.authentication import JWTStrategy

# OAuth2
from httpx_oauth.clients.google import GoogleOAuth2

from .manager import get_user_manager
from .models import User 
from config import SECRET_AUTH, GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET

google_oauth_client = GoogleOAuth2(
    GOOGLE_OAUTH_CLIENT_ID, 
    GOOGLE_OAUTH_CLIENT_SECRET)

# транспорт: то как токен будет передаваться по запросам
# Bearer предлагают для мобилок, 
# Легко читается и устанавливается в каждом запросе.
# Необходимо сохранить вручную где-нибудь в клиенте.
# Cookie для вэба 
# Автоматически сохраняется и безопасно отправляется веб-браузерами при каждом запросе.
# Автоматически удаляется веб-браузерами по истечении срока действия.
# Для максимальной безопасности требуется защита CSRF.
# Сложнее работать вне браузера, например, с мобильным приложением или сервером.
#bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
cookie_transport = CookieTransport(cookie_name='bonds', cookie_max_age=3600)

# стратегия: то как генерируется и защищается токен
# JWT(quick), Database and Redis(Custom, secure and performant)
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600)

# при проверке аут вызываются методы один за другим,
# первый метод вернувший пользователя выигрывает,
# если ни один не вернул пользователя вызывается ошибка
auth_backend = AuthenticationBackend(
    name='jwt',
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# возвращает юзера и проверяет аут
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# можно прикалываться с зависимостями
current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
is_auth_user = fastapi_users.current_user(optional=True)

async def auth_dependency_for_html(request: Request,
                           cur_user: User = Depends(is_auth_user)):
    context = {
        "cur_user": cur_user,
    }
    return context