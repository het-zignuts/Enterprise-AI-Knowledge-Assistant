from fastapi import FastAPI
from app.api.routes import router
from app.db.init_db import init_db

app=FastAPI(title="Enterprise AI Knowledge Assistant", version="1.0.0")

@app.on_event("startup") # Application startup hook.
def on_startup():
    init_db() # Establish database connections on startup

app.include_router(router)