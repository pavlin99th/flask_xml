import logging
from xml.sax import SAXException, parse

from flask_openapi3.models.file import FileStorage
from sqlalchemy import func, select
from sqlalchemy.orm import Session, sessionmaker

from db.storage import db
from models.entities import Attribute, File, Tag
from services.parser import XMLHandler

logger = logging.getLogger(__name__)


class XMLService:
    """Define XML service."""

    def __init__(self, db_session: sessionmaker[Session]) -> None:
        self.db = db_session

    def _check_file(self, session: Session, file_name: str) -> bool:
        """Test if given file exists in DB."""
        file = select(File).where(File.name == file_name)
        return session.scalar(file) is not None

    def process_file(self, file: FileStorage) -> bool | None:
        """Validate and save uploaded XML file to DB."""
        with self.db() as session:
            if self._check_file(session, file.filename):
                logger.error("File already exists: %s", file.filename)
                return None

            handler = XMLHandler(file.filename)
            try:
                parse(file, handler)
            except SAXException as err:
                logger.error("XML parsing failed: %r", err)
                return False
            session.add(handler.file)
            session.commit()
        logger.info("File added successfully: %s", file.filename)
        return True

    def count_tags(self, file_name: str, tag_name: str) -> int | None:
        """Count given tags in specified file."""
        with self.db() as session:
            if not self._check_file(session, file_name):
                logger.error("File not found: %s", file_name)
                return None

            query = (
                select(func.count(Tag.id))
                .join(File)
                .where(File.name == file_name, Tag.name == tag_name)
            )
            return session.scalar(query)

    def list_attributes(self, file_name: str, tag_name: str) -> list[str] | None:
        """List attributes for given tags in specified file."""
        with self.db() as session:
            if not self._check_file(session, file_name):
                logger.error("File not found: %s", file_name)
                return None

            query = (
                select(Attribute.name)
                .distinct()
                .join(Tag)
                .join(File)
                .where(File.name == file_name, Tag.name == tag_name)
            )
            return list(session.scalars(query).all())


xml_service = XMLService(db)
