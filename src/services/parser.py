from xml.sax.handler import ContentHandler
from xml.sax.xmlreader import AttributesImpl

from models.entities import Attribute, File, Tag


class XMLHandler(ContentHandler):
    """Define XML parser."""

    def __init__(self, file_name: str) -> None:
        super().__init__()
        self.file_name = file_name

    def startDocument(self) -> None:
        """Begin building File model."""
        self.file = File(name=self.file_name)

    def startElement(self, name: str, attrs: AttributesImpl) -> None:
        """Add tag and attributes to File model."""
        attributes = [Attribute(name=k, value=v) for k, v in attrs.items()]
        tag = Tag(name=name, attributes=attributes)
        self.file.tags.append(tag)
