from typing import Any, Dict, Optional, Union
from fastapi import HTTPException, status

class EntityNotFoundError(HTTPException):
    def __init__(self, entity_name: str, entity_id: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name} with ID {entity_id} not found."
        )

class RepositoryError(HTTPException):
    def __init__(self, detail: str = "Internal Database Error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
