from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LivroDTO(BaseDTO):
    id: int
    titulo: str
    autor: str
    isbn: str
    ano_publicacao: int


T = TypeVar('T', bound=BaseDTO)


class ResponseDTO(BaseModel, Generic[T]):
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None
