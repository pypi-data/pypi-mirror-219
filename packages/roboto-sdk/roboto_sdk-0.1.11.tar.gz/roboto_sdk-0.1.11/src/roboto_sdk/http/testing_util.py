import email.message
import io
import json
import typing
import urllib

from .http_client import HttpResponse


class FakeHttpResponseFactory:
    __headers: dict[str, str]
    __response_data: typing.Any
    __status_code: int
    __url: str

    def __init__(
        self,
        url: str,
        response_data: typing.Any,
        status_code: int = 200,
        headers: typing.Optional[dict[str, str]] = None,
    ) -> None:
        self.__status_code = status_code
        self.__headers = headers or dict()
        self.__response_data = response_data
        self.__url = url

    def __call__(self, *args, **kwargs) -> HttpResponse:
        headers = email.message.Message()
        for k, v in self.__headers.items():
            headers.add_header(k, v)
        data = io.BytesIO(json.dumps(self.__response_data).encode())
        urllib_response = urllib.response.addinfourl(
            data, headers, self.__url, self.__status_code
        )
        return HttpResponse(urllib_response)
