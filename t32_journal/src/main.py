import sentry_sdk
from collections import defaultdict
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

from src.config import app_configs, settings
from src.schemas import LogCreate
from src.service import save_log, get_logs

app = FastAPI(**app_configs)
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/log")
async def log(log_create: LogCreate):
    await save_log(log_create)
    return {"status": "Logged successfully"}


@app.get("/logs")
async def logs(request: Request,):
    logs_data = await get_logs()
    logs_by_user = defaultdict(list)
    for log_data in logs_data:
        logs_by_user[log_data["user"]].append(log_data)
    print(logs_by_user)
    return templates.TemplateResponse("logs.html", {"request": request, "logs_by_user": logs_by_user})

