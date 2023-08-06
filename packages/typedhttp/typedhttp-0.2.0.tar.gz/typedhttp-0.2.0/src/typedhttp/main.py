from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import (
    Callable,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
)


T = TypeVar("T")


class ResponseProvider(ABC):
    @abstractmethod
    def get_raw_response(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def iter_content(self, chunk_size: int) -> Iterator[bytes]:
        raise NotImplementedError

    @abstractmethod
    def get_headers(self) -> List[Tuple[str, str]]:
        raise NotImplementedError

    @abstractmethod
    def get_status_code(self) -> int:
        raise NotImplementedError


ResponseDecoder = Callable[[ResponseProvider], T]


@dataclass
class HTTPRequestObject(Generic[T]):
    method: str
    path: str
    response_decoder: ResponseDecoder[T]
    success_status_codes: List[int] = field(
        default_factory=lambda: [200, 201, 202, 203, 204, 205, 206, 207, 208, 226]
    )
    error_decoders: Dict[int, ResponseDecoder[Exception]] = field(default_factory=dict)
    as_stream: bool = False
    headers: Optional[List[Tuple[str, str]]] = None
    body: Optional[bytes] = None
    follow_redirects: bool = True
    basic_auth: Optional[Tuple[str, str]] = None


class HTTPHandler(ABC):
    @abstractmethod
    def send(self, request: HTTPRequestObject[T]) -> T:
        raise NotImplementedError

__all__ = [
    "HTTPHandler",
    "HTTPRequestObject",
    "ResponseDecoder",
    "ResponseProvider",
    "T",
]