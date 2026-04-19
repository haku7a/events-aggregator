import os

import uvicorn
from fastapi import FastAPI

from app.api.sync_routes import router as sync_router
from app.infrastructure.events_client import EventsProviderClient

app = FastAPI(title="Events Aggregator")
app.include_router(sync_router)

client = EventsProviderClient()


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
