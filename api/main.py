from fastapi import FastAPI
from routers import articles, categories, comments, users

app = FastAPI()

app.include_router(categories.router)