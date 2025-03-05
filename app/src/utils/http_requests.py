"""
Модуль создания HTTP запросов.
"""

from json import (
    JSONDecodeError,
    dumps as json_dumps,
)

from fastapi import status
from httpx import (
    AsyncClient,
    ConnectError as AsyncConnectError,
    ConnectTimeout as AsyncConnectTimeout,
    Headers as AsyncHeaders,
    LocalProtocolError as AsyncLocalProtocolError,
    ReadTimeout as AsyncReadTimeout,
    Response as AsyncResponse,
)


async def send_delete_request(
    url: str,
    headers: dict | None = None,
    auth: any = None,
    timeout: int = 15,
) -> tuple[int, dict[str, any] | None, AsyncHeaders | None]:
    """
    Отправляет DELETE запрос на указанный URL.

    Возвращает:
        - статус код ответа
        - тело ответа
        - заголовки ответа
    """
    return await __send_request(
        method='DELETE',
        url=url,
        headers=headers,
        auth=auth,
        timeout=timeout,
    )


async def send_post_request(
    url: str,
    data: dict | None = None,
    headers: dict | None = None,
    auth: any = None,
    timeout: int = 15,
) -> tuple[int, dict[str, any] | None, AsyncHeaders | None]:
    """
    Отправляет POST запрос на указанный URL с указанным телом запроса.

    Возвращает:
        - статус код ответа
        - тело ответа
        - заголовки ответа
    """
    return await __send_request(
        method='POST',
        url=url,
        data=data,
        headers=headers,
        auth=auth,
        timeout=timeout,
    )


async def send_get_request(
    url: str,
    headers: dict | None = None,
    auth: any = None,
    timeout: int = 15,
) -> tuple[int, dict[str, any] | None, AsyncHeaders | None]:
    """
    Отправляет GET запрос на указанный URL.

    Возвращает:
        - статус код ответа
        - тело ответа
        - заголовки ответа
    """
    return await __send_request(
        method='GET',
        url=url,
        headers=headers,
        auth=auth,
        timeout=timeout,
    )


async def __send_request(
    method: str,
    url: str,
    data: dict | None = None,
    headers: dict | None = None,
    auth: any = None,
    timeout: int = 15,
) -> tuple[int, dict[str, any] | None, AsyncHeaders | None]:
    """
    Отправляет HTTP запрос с указанными параметрами.

    Возвращает:
        - статус код ответа
        - тело ответа
        - заголовки ответа
    """
    if method not in ('DELETE', 'GET', 'POST'):
        raise ValueError(f'Метод {method} не поддерживается.')

    async with AsyncClient() as client:
        try:
            if method == 'DELETE':
                response: AsyncResponse = await client.delete(
                    url=url,
                    headers=headers,
                    auth=auth,
                    timeout=timeout,
                )
            elif method == 'GET':
                response: AsyncResponse = await client.get(
                    url=url,
                    headers=headers,
                    auth=auth,
                    timeout=timeout,
                )
            elif method == 'POST':
                response: AsyncResponse = await client.post(
                    url=url,
                    data=json_dumps(data) if data else None,
                    headers=headers,
                    auth=auth,
                    timeout=timeout,
                )
            response_status_code: int = response.status_code
            response_headers: AsyncHeaders = response.headers
            response_data: dict[str, any] = response.json()
        except AsyncConnectError:
            response_status_code: int = status.HTTP_504_GATEWAY_TIMEOUT
            response_headers: AsyncHeaders = None
            response_data: dict[str, any] = {
                'detail': 'Не удалось подключиться к серверу.',
            }
        except AsyncLocalProtocolError as e:
            response_status_code: int = status.HTTP_504_GATEWAY_TIMEOUT
            response_headers: AsyncHeaders = None
            response_data: dict[str, any] = {
                'detail': f'В запросе указаны некорректные данные заголовков: {e}',
            }
        except (AsyncConnectTimeout, AsyncReadTimeout):
            response_status_code: int = status.HTTP_504_GATEWAY_TIMEOUT
            response_headers: AsyncHeaders = None
            response_data: dict[str, any] = {
                'detail': f'Превышено время ожидания от сервера (timeout = {timeout} sec.).',
            }
        except JSONDecodeError:
            response_data: dict[str, any] = {'content': response.text}

    return (
        response_status_code,
        response_data,
        response_headers,
    )
