from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.User import user_router

import logging

logging.getLogger('passlib').setLevel(logging.ERROR)

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router.router)




