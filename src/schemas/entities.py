from flask_openapi3.models.file import FileStorage
from pydantic import BaseModel


class TagRequest(BaseModel):
    """Define tag request schema."""

    file_name: str
    tag_name: str


class UploadFileForm(BaseModel):
    """Define file upload schema."""

    file: FileStorage
