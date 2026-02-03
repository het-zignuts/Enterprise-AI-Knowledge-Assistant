from fastapi import FastAPI
from app.api.routes import router
from app.db.init_db import init_db

#FastAPI app instance with custom title and version in docs
app=FastAPI(title="Enterprise AI Knowledge Assistant", version="1.0.0")

@app.on_event("startup") # Application startup hook
def on_startup():
    init_db() # Establishing database connections on startup

# including API routes
app.include_router(router)