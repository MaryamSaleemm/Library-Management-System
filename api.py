from fastapi import FastAPI

from routers.users import router as user_router
from routers.books import router as books_router
from routers.loans import router as loans_router

app = FastAPI(
    title="Library Management API",
    version="1.0.0",
    description="Library Management System using FastAPI"
)

app.include_router(user_router)
app.include_router(books_router)
app.include_router(loans_router)



@app.get("/")
def root():
    return {
        "message": "Library Management API is Running"
    }
