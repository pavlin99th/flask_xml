import logging

from flask_openapi3.models.info import Info
from flask_openapi3.openapi import OpenAPI
from werkzeug.exceptions import HTTPException

from api import routes
from api.responses import handle_exception
from db.storage import init_db

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s %(message)s", level=logging.INFO)


def create_app() -> OpenAPI:
    """Build the main app."""
    info = Info(
        title="XML Service",
        version="1.0.0",
        description="API для обработки XML файлов и информации о тегах.",
    )
    app = OpenAPI(__name__, info=info)
    app.register_api(routes.api)
    app.register_error_handler(HTTPException, handle_exception)
    init_db()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
