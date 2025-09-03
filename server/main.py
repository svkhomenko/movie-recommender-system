import uvicorn
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from routers import root_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CLIENT_URL") or "http://localhost"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization", "Set-Cookie"],
    expose_headers=["X-Total-Count"],
)

app.include_router(root_router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=(os.getenv("SERVER_HOST") or "localhost"),
        port=int(os.getenv("SERVER_PORT") or 8000),
    )
