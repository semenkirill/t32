from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = "SECRET"
    JWT_EXP: int = 5  # minutes

    REFRESH_TOKEN_KEY: str = "refreshToken"
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21  # 21 days

    SECURE_COOKIES: bool = True


auth_config = AuthConfig()
