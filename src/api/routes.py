from http import HTTPStatus

from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag

from api.responses import (
    ApiBoolResponse,
    ApiErrorResponse,
    ApiIntResponse,
    ApiListResponse,
    JSONResponse,
    json_response,
)
from schemas.entities import TagRequest, UploadFileForm
from services.xml_service import xml_service

api = APIBlueprint(
    "xml",
    __name__,
    url_prefix="/api/",
    abp_tags=[Tag(name="XML endpoints")],
)


@api.post(
    "/file/read",
    summary="Чтение XML файла",
    description="Валидирует и сохраняет принятый XML файл в БД.",
    responses={
        HTTPStatus.OK: ApiBoolResponse,
        HTTPStatus.CONFLICT: ApiBoolResponse,
        HTTPStatus.UNPROCESSABLE_ENTITY: ApiBoolResponse,
    },
)
def save_xml(form: UploadFileForm) -> JSONResponse:
    """Validate and save XML file to DB."""
    status = xml_service.process_file(form.file)
    if status is None:
        return json_response(ApiErrorResponse(msg="Файл уже существует"), HTTPStatus.CONFLICT)
    code = HTTPStatus.OK if status else HTTPStatus.UNPROCESSABLE_ENTITY
    return json_response(ApiBoolResponse(result=status), code)


@api.get(
    "/tags/get-count",
    summary="Количество тегов в файле",
    description="Возвращает количество указанных тегов в заданном файле.",
    responses={
        HTTPStatus.OK: ApiIntResponse,
        HTTPStatus.NOT_FOUND: ApiErrorResponse,
    },
)
def count_tags(query: TagRequest) -> JSONResponse:
    """Count given tag in specified file."""
    count = xml_service.count_tags(query.file_name, query.tag_name)
    if count is None:
        return json_response(ApiErrorResponse(msg="Файл не найден"), HTTPStatus.NOT_FOUND)

    if count > 0:
        return json_response(ApiIntResponse(result=count), HTTPStatus.OK)
    return json_response(
        ApiErrorResponse(msg="В файле отсутствует тег с данным названием"),
        HTTPStatus.NOT_FOUND,
    )


@api.get(
    "/tags/attributes/get",
    summary="Список атрибутов",
    description="Возвращает список атрибутов для указанного тега в заданном файле.",
    responses={
        HTTPStatus.OK: ApiListResponse,
        HTTPStatus.NOT_FOUND: ApiErrorResponse,
    },
)
def list_attributes(query: TagRequest) -> JSONResponse:
    """List attributes for given tag in specified file."""
    attrs = xml_service.list_attributes(query.file_name, query.tag_name)
    if attrs is None:
        return json_response(ApiErrorResponse(msg="Файл не найден"), HTTPStatus.NOT_FOUND)

    return json_response(ApiListResponse(result=attrs), HTTPStatus.OK)
