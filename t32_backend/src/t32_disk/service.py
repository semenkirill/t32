from pathlib import Path
from typing import List, Dict, Any

from fastapi import UploadFile, HTTPException
from uuid import uuid4

from src.database import files, execute, fetch_one, fetch_all


async def save_file(user_id: int, file: UploadFile):
    # Генерация UUID для файла
    file_uuid = str(uuid4())

    # Запись информации о файле в базу данных
    insert_query = files.insert().values(
        uuid=file_uuid,
        user_id=user_id,
        filename=file.filename,
        content_type=file.content_type
    )
    await execute(insert_query)

    # Сохранение файла на диск
    user_folder = Path(f"uploads/{user_id}")
    if not user_folder.exists():
        user_folder.mkdir(parents=True)

    file_path = user_folder / file.filename
    with file_path.open("wb") as f:
        f.write(file.file.read())

    return {"message": f"File '{file.filename}' saved successfully", "path": str(file_path)}


async def delete_file(user_id: int, file_uuid: str):
    # Проверка наличия файла в базе данных
    select_query = files.select().where(
        (files.c.user_id == user_id) &
        (files.c.uuid == file_uuid)
    )
    existing_file = await fetch_one(select_query)

    if existing_file:
        # Удаление файла из базы данных
        delete_query = files.delete().where(
            (files.c.user_id == user_id) &
            (files.c.uuid == file_uuid)
        )
        await execute(delete_query)

        # Удаление файла с диска
        user_folder = Path(f"uploads/{user_id}")
        file_path = user_folder / existing_file['filename']
        if file_path.exists():
            file_path.unlink()

        return {"message": f"File deleted successfully"}
    else:
        return {"message": f"File not found"}


async def get_user_files(user_id: int) -> list[dict[str, Any]]:
    select_query = files.select().where(files.c.user_id == user_id)
    user_files = await fetch_all(select_query)
    return user_files


async def download_file(user_id: int, file_uuid: str):
    select_query = files.select().where(
        (files.c.user_id == user_id) &
        (files.c.uuid == file_uuid)
    )
    existing_file = await fetch_one(select_query)

    if existing_file:
        user_folder = Path(f"uploads/{user_id}")
        file_path = user_folder / existing_file['filename']
        return file_path
    else:
        raise HTTPException(status_code=404, detail="File not found")

async def get_path_file(file_uuid: str):
    select_query = files.select().where(
        (files.c.uuid == file_uuid)
    )
    existing_file = await fetch_one(select_query)

    if existing_file:
        user_folder = Path(f"uploads/{existing_file['user_id']}")
        file_path = user_folder / existing_file['filename']
        return file_path
    else:
        raise HTTPException(status_code=404, detail="File not found")

