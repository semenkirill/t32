from src.database import log, execute
from src.schemas import LogCreate

from src.database import fetch_all


async def save_log(log_create: LogCreate):
    insert_query = log.insert().values(
        user=log_create.user,
        log_type=log_create.type,
        message=log_create.message,
    )
    await execute(insert_query)
    return {"message": "success"}


async def get_logs():
    query = log.select().order_by(log.c.created_at.desc())
    result = await fetch_all(query)
    return result
