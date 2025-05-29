from fastapi import FastAPI
from routers import articles, categories, comments, users

app = FastAPI()

app.include_router(categories.router)
app.include_router(articles.router)
app.include_router(users.router)
app.include_router(comments.router)