from fastapi import FastAPI
from microservices.auth.routers.auth_routes import router

app = FastAPI()

app.include_router(router)