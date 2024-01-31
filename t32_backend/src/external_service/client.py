import httpx

from src.external_service.schemas import LogCreate


class Client:
    """
    This is the client to Public APIs service,
    which returns the list of APIs with public access.
    """

    BASE_URL: str = "http://t32_journal:8001"

    @property
    def client(self):
        return httpx.AsyncClient(base_url=self.BASE_URL, timeout=10.0)

    async def send_log(self, log_create:LogCreate) -> None:
        async with self.client as client:
            print(self.BASE_URL)
            try:
                response = await client.post("/log", json=log_create.model_dump())
                print(response.json())
            except Exception as e:
                print(e)

