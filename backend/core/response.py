from fastapi import status
from fastapi.responses import JSONResponse


class ApiResponse:
    def __init__(self, status_code: int = status.HTTP_200_OK, message: str = None, data: dict = None):
        self.status_code = status_code
        self.message = message
        self.data = data

    def to_http_response(self):
        return JSONResponse(
            status_code=self.status_code,
            content={
                "success": {
                    "message": self.message,
                    "data": self.data
                }
            }
        )

    @classmethod
    def success(cls, message="Request successful", data=None):
        return cls(status.HTTP_200_OK, message, data)

    @classmethod
    def created(cls, message="Created", data=None):
        return cls(status.HTTP_201_CREATED, message, data)

    @classmethod
    def no_content(cls, message="No content", data=None):
        return cls(status.HTTP_204_NO_CONTENT, message, data)