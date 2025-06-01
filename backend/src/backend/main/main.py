import uvicorn
from fastapi import FastAPI

from src.backend.main.config import config
from src.backend.main.setup.setup_app import setup

from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup(app)
    return app



if __name__ == "__main__":
    uvicorn.run(
        app=create_app(),
        host=config.app.host,
        port=config.app.port,
    )
