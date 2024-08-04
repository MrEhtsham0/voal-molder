from fastapi import FastAPI
from routers.api import router
from utils.init_db import create_tables
from utils.logger import logging

app = FastAPI()
@app.on_event("startup")
def on_startup() -> None:
    create_tables()
    logging.info("Table has created Sucessfully...")

app.include_router(router=router)

