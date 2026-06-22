"""src/core/exceptions.py."""

from typing import Any

from pydantic import BaseModel
from pydantic import Field


class ErrorResponseSchema(BaseModel):
    """Standardized error response format for the frontend."""

    error_code: str = Field(
        ..., description="Unique error code for the frontend to switch on"
    )
    message: str = Field(..., description="Human-readable error message")


class AppError(Exception):
    """Base exception for all application-level errors."""

    def __init__(
        self, message: str, status_code: int = 400, error_code: str = "BAD_REQUEST"
    ):
        """Initialize base app error."""
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class ClientNotFoundError(AppError):
    """Client not found error."""

    def __init__(self):
        """Initialize client not found error."""
        super().__init__(
            "Client not found", status_code=404, error_code="CLIENT_NOT_FOUND"
        )


class ProductNotFoundError(AppError):
    """Product not found error."""

    def __init__(self):
        """Initialize product not found error."""
        super().__init__(
            "Product not found", status_code=404, error_code="PRODUCT_NOT_FOUND"
        )


class OrderNotFoundError(AppError):
    """Order not found error."""

    def __init__(self):
        """Initialize order not found error."""
        super().__init__(
            "Order not found", status_code=404, error_code="ORDER_NOT_FOUND"
        )


class AuthenticationFailedError(AppError):
    """Authentication failed error."""

    def __init__(self):
        """Initialize authentication failed error."""
        super().__init__(
            "Authentication failed", status_code=401, error_code="UNAUTHORIZED"
        )


class PermissionDeniedError(AppError):
    """Permission denied error."""

    def __init__(self):
        """Initialize permission denied error."""
        super().__init__("Permission denied", status_code=403, error_code="FORBIDDEN")


class ValidationError(AppError):
    """Validation error."""

    def __init__(self):
        """Initialize validation error."""
        super().__init__(
            "Validation Error", status_code=422, error_code="VALIDATION_ERROR"
        )


class InternalServerError(AppError):
    """Internal server error."""

    def __init__(self):
        """Initialize internal server error."""
        super().__init__(
            "An unexpected error occurred",
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR",
        )


def create_error_responses(*exceptions: type[AppError]) -> dict[int, dict[str, Any]]:
    """Generate OpenAPI response schemas for given AppError classes."""
    responses = {}
    for exc in exceptions:
        # Create an instance to access default values
        instance = exc()
        if instance.status_code not in responses:
            responses[instance.status_code] = {
                "description": instance.message,
                "model": ErrorResponseSchema,
                "content": {"application/json": {"examples": {}}},
            }
        # If multiple errors share the same status code, append their descriptions
        elif instance.message not in responses[instance.status_code]["description"]:
            responses[instance.status_code]["description"] += f" | {instance.message}"

        responses[instance.status_code]["content"]["application/json"]["examples"][
            instance.error_code
        ] = {
            "summary": instance.message,
            "value": {"error_code": instance.error_code, "message": instance.message},
        }
    return responses


COMMON_ERROR_CLASSES = (ValidationError, InternalServerError)
