from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import api_router


app = FastAPI()

app.mount('/media', StaticFiles(directory='media'), name='media')
app.include_router(api_router)
