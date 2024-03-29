import sentry_sdk
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.t32_disk.router import router as t32_disk_router
from src.config import app_configs, settings
from fastapi.templating import Jinja2Templates

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
    expose_headers=["Content-Disposition"]
)

if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )

templates = Jinja2Templates(directory="templates")


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(t32_disk_router, prefix="/t32_disk", tags=["T32 Disk Router"])
