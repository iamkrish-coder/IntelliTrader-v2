from fastapi import status
from fastapi.responses import JSONResponse


class ApiException(Exception):
    def __init__(self, status_code: int = status.HTTP_200_OK, message: str = None, data: dict = None):
        self.status_code = status_code
        self.message = message
        self.data = data

    def to_http_exception(self):
        return JSONResponse(
            status_code=self.status_code,
            content={
                "error": {
                    "message": self.message,
                    "data": self.data
                }
            }
        )

    @classmethod
    def invalid_data_type_error(cls, message="Invalid data types provided", data=None):
        return cls(status.HTTP_400_BAD_REQUEST, message, data)

    @classmethod
    def bad_request_error(cls, message="Bad request", data=None):
        return cls(status.HTTP_400_BAD_REQUEST, message, data)

    @classmethod
    def unauthorized_error(cls, message="Unauthorized access", data=None):
        return cls(status.HTTP_401_UNAUTHORIZED, message, data)

    @classmethod
    def forbidden_error(cls, message="Forbidden", data=None):
        return cls(status.HTTP_403_FORBIDDEN, message, data)

    @classmethod
    def not_found_error(cls, message="Resource not found", data=None):
        return cls(status.HTTP_404_NOT_FOUND, message, data)

    @classmethod
    def conflict_error(cls, message="Resource conflict", data=None):
        return cls(status.HTTP_409_CONFLICT, message, data)

    @classmethod
    def validation_error(cls, message="Validation failed", data=None):
        return cls(status.HTTP_422_UNPROCESSABLE_ENTITY, message, data)

    @classmethod
    def unprocessable_entity_error(cls, message="Unprocessable entity", data=None):
        return cls(status.HTTP_422_UNPROCESSABLE_ENTITY, message, data)

    @classmethod
    def too_many_requests_error(cls, message="Too many requests", data=None):
        return cls(status.HTTP_429_TOO_MANY_REQUESTS, message, data)

    @classmethod
    def internal_server_error(cls, message="Internal server error", data=None):
        return cls(status.HTTP_500_INTERNAL_SERVER_ERROR, message, data)

    @classmethod
    def not_implemented_error(cls, message="Not implemented", data=None):
        return cls(status.HTTP_501_NOT_IMPLEMENTED, message, data)

    @classmethod
    def service_unavailable_error(cls, message="Service unavailable", data=None):
        return cls(status.HTTP_503_SERVICE_UNAVAILABLE, message, data)

    @classmethod
    def gateway_timeout_error(cls, message="Gateway timeout", data=None):
        return cls(status.HTTP_504_GATEWAY_TIMEOUT, message, data)

    @classmethod
    def database_error(cls, message="Database operation failed", data=None):
        """Handle database-specific errors with internal server error status."""
        return cls(status.HTTP_500_INTERNAL_SERVER_ERROR, message, data)