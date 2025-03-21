from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Define base for models."""

    pass


class File(Base):
    """Describe File table."""

    __tablename__ = "Files"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text(), unique=True)

    tags: Mapped[list["Tag"]] = relationship()

    def __repr__(self) -> str:
        return f"File(id={self.id}, name={self.name})"


class Tag(Base):
    """Describe Tag table."""

    __tablename__ = "Tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    file_id = mapped_column(ForeignKey("Files.id"))

    attributes: Mapped[list["Attribute"]] = relationship()

    def __repr__(self) -> str:
        return f"Tag(id={self.id}, name={self.name}, file_id={self.file_id})"


class Attribute(Base):
    """Describe Attribute table."""

    __tablename__ = "Attributes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text())
    value: Mapped[str] = mapped_column(Text())
    tag_id = mapped_column(ForeignKey("Tags.id"))

    def __repr__(self) -> str:
        return f"Attribute(id={self.id}, name={self.name}, tag_id={self.tag_id})"
