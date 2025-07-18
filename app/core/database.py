import mongoengine as me
from sqlalchemy import create_engine
from app.core.config import settings
from sqlalchemy.orm import sessionmaker
from app.models.user import Base

SessionLocal = None

def create_tables(engine):
    global SessionLocal
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)


def get_psql():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def connect_mongo():
    me.connect(
    db=settings.MONGO_DB,
    host=settings.MONGO_HOST,
    port=settings.MONGO_PORT,
    alias="default"  # por si usas múltiples conexiones
)
    print("[MongoDB] Connected.")

def connect_postgres():
    url = (
        f"postgresql+psycopg2://{settings.POSTGRES_USER}:"
        f"{settings.POSTGRES_PASSWORD}@"
        f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/"
        f"{settings.POSTGRES_DB}"
    )
    engine = create_engine(url, echo=True)
    print("[PostgreSQL] Connected.")
    return engine
