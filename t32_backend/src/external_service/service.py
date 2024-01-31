
from src.external_service.client import Client
from src.external_service.schemas import LogCreate


async def send_client_log(user:str|int, message:str):
    client = Client()
    await client.send_log(
        LogCreate(
            user=str(user),
            message=message,
            type='client'
        )
    )

async def send_server_log(user:str|int, message:str):
    client = Client()
    await client.send_log(
        LogCreate(
            user=str(user),
            message=message,
            type='server'
        )
    )