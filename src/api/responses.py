from http import HTTPStatus
from typing import Any

from pydantic import BaseModel


class ApiErrorResponse(BaseModel):
    """Define API error response schema."""

    msg: str


class ApiBoolResponse(BaseModel):
    """Define API boolean response schema."""

    result: bool


class ApiIntResponse(BaseModel):
    """Define API int response schema."""

    result: int


class ApiListResponse(BaseModel):
    """Define API list response schema."""

    result: list[str]


JSONResponse = tuple[dict[str, Any], HTTPStatus]


def json_response(model: BaseModel, code: HTTPStatus) -> JSONResponse:
    """Return Pydantic model as JSON response with status code."""
    return model.model_dump(), code


def handle_exception(*args: Any) -> JSONResponse:
    """Report internal service error."""
    return json_response(
        ApiErrorResponse(msg="Internal server error"), HTTPStatus.INTERNAL_SERVER_ERROR
    )


ResponseMap = dict[HTTPStatus, type[BaseModel]]

response_ok_bool: ResponseMap = {HTTPStatus.OK: ApiBoolResponse}
response_ok_int: ResponseMap = {HTTPStatus.OK: ApiIntResponse}
response_ok_list: ResponseMap = {HTTPStatus.OK: ApiListResponse}

response_not_found: ResponseMap = {HTTPStatus.NOT_FOUND: ApiErrorResponse}
response_conflict: ResponseMap = {HTTPStatus.CONFLICT: ApiErrorResponse}
response_unprocessable: ResponseMap = {HTTPStatus.UNPROCESSABLE_ENTITY: ApiErrorResponse}
