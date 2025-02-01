from fastapi import Request
from starlette.responses import JSONResponse
import time
import uuid

from backend.core.exceptions import ApiException
from backend.utils.logging_utils import log_error, log_info

async def error_handling_middleware(request: Request, call_next):
    """Global middleware for handling errors and adding request context."""
    
    # Generate unique request ID
    request_id = str(uuid.uuid4())
    # Record start time
    start_time = time.time()
    
    try:
        # Add request ID to request state
        request.state.request_id = request_id
        
        # Log incoming request
        log_info(f"Request {request_id}: {request.method} {request.url}")
        
        # Process the request
        response = await call_next(request)
        
        # Calculate request duration
        duration = time.time() - start_time
        log_info(f"Request {request_id} completed in {duration:.2f}s")
        
        return response
        
    except ApiException as error:
        # Handle known API exceptions
        duration = time.time() - start_time
        log_error(
            f"Request {request_id} failed in {duration:.2f}s: "
            f"{error.__class__.__name__}: {str(error)}"
        )
        
        # Create error response with request context
        return JSONResponse(
            status_code=error.status_code,
            content={
                "error": {
                    "message": error.message,
                    "data": error.data,
                    "request_id": request_id,
                    "path": str(request.url),
                    "method": request.method
                }
            }
        )
        
    except Exception as e:
        # Handle unexpected exceptions
        duration = time.time() - start_time
        log_error(
            f"Request {request_id} failed with unexpected error in {duration:.2f}s: "
            f"{e.__class__.__name__}: {str(e)}"
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "message": "An unexpected error occurred",
                    "data": {
                        "error_type": e.__class__.__name__,
                        "error_details": str(e)
                    },
                    "request_id": request_id,
                    "path": str(request.url),
                    "method": request.method
                }
            }
        )
