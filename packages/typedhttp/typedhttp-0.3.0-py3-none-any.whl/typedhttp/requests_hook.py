from typing import Iterator, List, Tuple, TypeVar

import requests

from typedhttp import HTTPHandler, HTTPRequestObject, ResponseProvider

from typedhttp.exc import NoExceptionProvidedForStatusCode

T = TypeVar("T")


class RequestsResponseProvider(ResponseProvider):
    def __init__(self, response: requests.Response) -> None:
        self.response = response

    def get_raw_response(self) -> bytes:
        return self.response.content

    def iter_content(self, chunk_size: int) -> Iterator[bytes]:
        return self.response.iter_content(chunk_size=chunk_size)

    def get_headers(self) -> List[Tuple[str, str]]:
        return [
            (header_name, header_value)
            for header_name, header_value in self.response.headers.items()
        ]

    def get_status_code(self) -> int:
        return self.response.status_code


class RequestsHTTPHandler(HTTPHandler):
    def __init__(self, session: requests.Session, url: str) -> None:
        self.session = session
        self.url = url

    def send(self, request: HTTPRequestObject[T]) -> T:
        response = self.session.request(
            method=request.method,
            url=self.url + request.path,
            headers={header[0]: header[1] for header in request.headers}
            if request.headers is not None
            else None,
            data=request.body,
            stream=request.as_stream,
            allow_redirects=request.follow_redirects,
            auth=request.basic_auth,
        )

        response_provider = RequestsResponseProvider(response)

        if response.status_code not in request.success_status_codes:
            if response.status_code in request.error_decoders:
                request.error_decoders[response.status_code](response_provider)

            else:
                raise NoExceptionProvidedForStatusCode(
                    f"Request failed with status code {response.status_code} and no error decoder: {response.text}"
                )

        return request.response_decoder(response_provider)


__all__ = ["RequestsHTTPHandler", "RequestsResponseProvider"]
