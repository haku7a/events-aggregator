import asyncio
import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.events_routes import router as events_router
from app.api.seats_routes import router as seats_router
from app.api.sync_routes import router as sync_router
from app.api.tickets_routes import router as tickets_router
from app.db.repositories import EventRepository, SyncStateRepository
from app.db.session import AsyncSessionLocal
from app.infrastructure.events_client import EventsProviderClient
from app.usecases import SyncEventsUsecase

logger = logging.getLogger(__name__)

client = EventsProviderClient()
sync_task: asyncio.Task | None = None


async def periodic_sync():
    await asyncio.sleep(10)
    while True:
        try:
            async with AsyncSessionLocal() as session:
                event_repo = EventRepository(session)
                sync_repo = SyncStateRepository(session)
                usecase = SyncEventsUsecase(
                    client=client, event_repo=event_repo, sync_repo=sync_repo
                )
                count = await usecase.execute()
                await session.commit()
                logger.info("Periodic sync completed: %d events", count)
        except Exception:
            logger.exception("Periodic sync failed")
        await asyncio.sleep(86400)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global sync_task
    sync_task = asyncio.create_task(periodic_sync())
    yield
    if sync_task:
        sync_task.cancel()
        try:
            await sync_task
        except asyncio.CancelledError:
            pass
    await client.close()


app = FastAPI(title="Events Aggregator", lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


app.include_router(sync_router)
app.include_router(events_router)
app.include_router(seats_router)
app.include_router(tickets_router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
