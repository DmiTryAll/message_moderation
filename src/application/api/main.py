from contextlib import asynccontextmanager

from aiojobs import Scheduler
from fastapi import FastAPI
from punq import Container

from application.api.utils.lifespan import moderate
from application.api.v1 import v1_router
from application.container import init_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = init_container()

    scheduler: Scheduler = container.resolve(Scheduler)

    job = await scheduler.spawn(moderate())

    yield

    await job.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Message Moderation",
        docs_url="/docs",
        description="",
        debug=True,
        lifespan=lifespan,
        root_path="/api"
    )
    app.include_router(v1_router, prefix="/v1")

    return app