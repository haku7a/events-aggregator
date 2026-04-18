import os

import uvicorn
from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(title="Events Aggregator")


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    test = settings.POSTGRES_PORT
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
