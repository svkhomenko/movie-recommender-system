from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def validation_exception_handler(_: Request, exc: RequestValidationError):
    error_messages = []

    for error in exc.errors():
        field = " -> ".join(map(str, error["loc"][1:]))
        message = f"Field '{field}': {error['msg']}"
        error_messages.append(message)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": error_messages[0], "errors": error_messages},
    )


def register_exception_handlers(app):
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
