from databases import Database
from sqlalchemy import create_engine, MetaData
from core.config import Settings

settings = Settings()

database = Database(settings.database_url)
metadata = MetaData()
engine = create_engine(
    settings.database_url,
)