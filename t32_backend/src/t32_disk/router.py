from fastapi import APIRouter, UploadFile, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from .service import save_file, delete_file, get_user_files, download_file
from ..auth.jwt import parse_jwt_user_data
from ..auth.schemas import JWTData
from ..external_service.service import send_client_log, send_server_log

router = APIRouter()


@router.post("/upload_files/", response_model=dict)
async def upload_file(files: list[UploadFile], background_tasks: BackgroundTasks, jwt_data: JWTData = Depends(parse_jwt_user_data)):
    background_tasks.add_task(send_client_log, jwt_data.user_id, f"Клиент загружает на сервер {len(files)} файла(ов)")
    for file in files:
        saved_file = await save_file(user_id=jwt_data.user_id, file=file)
    background_tasks.add_task(send_server_log, jwt_data.user_id, f"Клиент загрузил на сервер {len(files)} файла(ов)")
    return {"message": "Files uploaded"}


@router.delete("/delete_files/{file_uuid}/", response_model=dict)
async def delete_uploaded_file(file_uuid: str, background_tasks: BackgroundTasks, jwt_data: JWTData = Depends(parse_jwt_user_data)):
    background_tasks.add_task(send_client_log, jwt_data.user_id, f"Клиент пытается удалить {file_uuid} файл")
    result = await delete_file(jwt_data.user_id, file_uuid)
    background_tasks.add_task(send_server_log, jwt_data.user_id, f"Клиент  удалил {file_uuid} файл")
    return result


@router.get("/user_files/", response_model=list[dict])
async def get_user_uploaded_files(background_tasks: BackgroundTasks, jwt_data: JWTData = Depends(parse_jwt_user_data)):
    background_tasks.add_task(send_client_log, jwt_data.user_id, "Клиент пытается получить список файлов")
    user_files = await get_user_files(jwt_data.user_id)
    background_tasks.add_task(send_server_log, jwt_data.user_id, "Клиент получил список файлов")
    return user_files


@router.get("/download_file/{file_uuid}/", response_class=FileResponse)
async def download_uploaded_file(file_uuid: str, background_tasks: BackgroundTasks, jwt_data: JWTData = Depends(parse_jwt_user_data)):
    background_tasks.add_task(send_client_log, jwt_data.user_id, f"Клиент пытается скачать файл {file_uuid}")
    file_path = await download_file(jwt_data.user_id, file_uuid)
    background_tasks.add_task(send_server_log, jwt_data.user_id, f"Клиент скачал файл {file_uuid}")
    return FileResponse(file_path, filename=file_path.name)
