import logging
import logging.config
import sys

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .dependencies.auth import login_required

from .middlewares.logging import LoggingMiddleware
from .settings import settings
from .routers import file, context, project, embeddings, auth

logging_config = {
    "version": 1,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(process)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)s",
        }
    },
    "handlers": {
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": sys.stderr,
        }
    },
    "root": {"level": "DEBUG", "handlers": ["console"], "propagate": True},
}

logging.config.dictConfig(logging_config)

app = FastAPI(name="Arkive Web Service", debug=True)

app.add_middleware(
    LoggingMiddleware,
    logger=logging.getLogger(__name__),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file.router, dependencies=[Depends(login_required)])
app.include_router(context.router, dependencies=[Depends(login_required)])
app.include_router(project.router, dependencies=[Depends(login_required)])
app.include_router(embeddings.router, dependencies=[Depends(login_required)])
app.include_router(auth.router)


def main():
    uvicorn.run(
        "api_service.__main__:app", host="0.0.0.0", port=8000, reload=True
    )