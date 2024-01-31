from typing import Any
from fastapi import APIRouter, BackgroundTasks, Depends, Response, status

from src.auth import jwt, service, utils
from src.auth.dependencies import (
    valid_refresh_token,
    valid_refresh_token_user,
    valid_user_create,
)
from src.auth.jwt import parse_jwt_user_data
from src.auth.schemas import AccessTokenResponse, AuthUser, JWTData, UserResponse
from src.external_service.service import send_client_log, send_server_log

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
    auth_data: AuthUser = Depends(valid_user_create),
) -> dict[str, str]:
    user = await service.create_user(auth_data)
    return {
        "email": user["email"],
    }


@router.get("/users/me", response_model=UserResponse)
async def get_my_account(
    background_tasks: BackgroundTasks,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    background_tasks.add_task(send_client_log, jwt_data.user_id, "Получение данных об емаил")
    user = await service.get_user_by_id(jwt_data.user_id)
    background_tasks.add_task(send_server_log, jwt_data.user_id, "Получение данных об емаил")
    return {
        "email": user["email"],
    }


@router.post("/users/tokens", response_model=AccessTokenResponse)
async def auth_user(auth_data: AuthUser, response: Response, background_tasks: BackgroundTasks) -> AccessTokenResponse:
    background_tasks.add_task(send_client_log, auth_data.email, "Попытка авторизации")
    user = await service.authenticate_user(auth_data)
    background_tasks.add_task(send_client_log, auth_data.email, "Успешная авторизация")
    refresh_token_value = await service.create_refresh_token(user_id=user["id"])

    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))
    background_tasks.add_task(send_server_log, auth_data.email, "Установили cookie")
    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.put("/users/tokens", response_model=AccessTokenResponse)
async def refresh_tokens(
    worker: BackgroundTasks,
    response: Response,
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
    user: dict[str, Any] = Depends(valid_refresh_token_user),
) -> AccessTokenResponse:
    refresh_token_value = await service.create_refresh_token(
        user_id=refresh_token["user_id"]
    )
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    worker.add_task(service.expire_refresh_token, refresh_token["uuid"])
    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.delete("/users/tokens")
async def logout_user(
    response: Response,
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
) -> None:
    await service.expire_refresh_token(refresh_token["uuid"])

    response.delete_cookie(
        **utils.get_refresh_token_settings(refresh_token["refresh_token"], expired=True)
    )