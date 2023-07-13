from fastapi import FastAPI
from ratelimit import RateLimitMiddleware, Rule
from ratelimit.backends.simple import MemoryBackend

from app.api.api_v1.api import api_router
from app.limit.auths import all_users_rps


def get_application() -> FastAPI:
    application = FastAPI(title="Yandex Lavka")
    application.include_router(api_router)
    application.add_middleware(
        RateLimitMiddleware,
        authenticate=all_users_rps,
        backend=MemoryBackend(),
        config={
            r"^/*": [Rule(second=10)],
        },
    )

    return application


app = get_application()
