import logging
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from models.entities import Base

engine = create_engine(f"sqlite:///{settings.sqlite_folder}/{settings.sqlite_db}")
db = sessionmaker(engine)
if settings.sqlalchemy_echo:
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def init_db() -> None:
    """Create DB tables."""
    Path(settings.sqlite_folder).mkdir(exist_ok=True)
    Base.metadata.create_all(engine)
