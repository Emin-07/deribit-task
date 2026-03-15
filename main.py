from fastapi import FastAPI

from routes.price_routes import router as price_router

app = FastAPI()

app.include_router(price_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
