from fastapi import FastAPI

from database import Base, engine
from routers import auth, todos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ToDo API", version="1.0.0")

app.include_router(auth.router)
app.include_router(todos.router)


@app.get("/")
def root():
    return {"message": "ToDo API - visit /docs for API documentation"}
