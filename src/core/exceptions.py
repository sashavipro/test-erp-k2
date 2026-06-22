from typing import Dict, Any, Type

class AppError(Exception):
    """Base exception for all application-level errors."""
    def __init__(self, message: str, status_code: int = 400, error_code: str = "BAD_REQUEST"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

class ClientNotFoundError(AppError):
    def __init__(self):
        super().__init__("Client not found", status_code=404, error_code="CLIENT_NOT_FOUND")

class ProductNotFoundError(AppError):
    def __init__(self):
        super().__init__("Product not found", status_code=404, error_code="PRODUCT_NOT_FOUND")

class OrderNotFoundError(AppError):
    def __init__(self):
        super().__init__("Order not found", status_code=404, error_code="ORDER_NOT_FOUND")

class AuthenticationFailedError(AppError):
    def __init__(self):
        super().__init__("Authentication failed", status_code=401, error_code="UNAUTHORIZED")

class PermissionDeniedError(AppError):
    def __init__(self):
        super().__init__("Permission denied", status_code=403, error_code="FORBIDDEN")


def create_error_responses(*exceptions: Type[AppError]) -> Dict[int, Dict[str, Any]]:
    """
    Generates OpenAPI response schemas for given AppError classes.
    """
    responses = {}
    for exc in exceptions:
        # Create an instance to access default values
        instance = exc()
        responses.setdefault(instance.status_code, {
            "description": "Error",
            "content": {
                "application/json": {
                    "examples": {}
                }
            }
        })
        
        responses[instance.status_code]["content"]["application/json"]["examples"][instance.error_code] = {
            "summary": instance.message,
            "value": {
                "error_code": instance.error_code,
                "message": instance.message
            }
        }
    return responses
