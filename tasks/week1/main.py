# main.py
from fastapi import FastAPI
from infra import web_adapter

app = FastAPI()
app.include_router(web_adapter.user_router)