import os

import uvicorn
from fastapi import FastAPI



import sys



app = FastAPI(title="Events Aggregator")


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
