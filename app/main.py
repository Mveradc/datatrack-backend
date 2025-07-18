from fastapi import FastAPI
from app.core.config import settings
from app.core.database import connect_mongo, connect_postgres, create_tables

app = FastAPI(title="DataTrack Core API", version="0.1.0")


@app.on_event("startup")
async def startup():
    connect_mongo()
    postgres_engine = connect_postgres()
    create_tables(postgres_engine)
