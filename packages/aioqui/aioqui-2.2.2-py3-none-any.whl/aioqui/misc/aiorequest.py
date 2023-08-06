from typing import Optional, Union, Dict, List
from aiohttp import ClientSession
from contextlib import suppress
from ast import literal_eval
from typing import Any
from uuid import UUID
from datetime import datetime
import ujson

from .utils import aiocache

# ToDo: "TypeError: unhashable type: 'dict'"


JsonProcessed: type = Optional[
    Union[
        Dict[str, 'JsonProcessed'], List['JsonProcessed'], str, int, float, bool, UUID, datetime
    ]
]
baseurl: Optional[str] = None


async def request(
        method: str, url: str,
        /,
        *,
        params: dict[str, Any] = None,
        headers: dict[str, Any] = None,
        body: dict[str, Any] = None,
        data: dict[str, Any] = None,
        deserialize: bool = False
) -> Any:
    if params:  # convert params values to str
        params = {key: str(value) for key, value in params.items()}
    if (method := method.lower()) not in ('get', 'post', 'put', 'delete'):
        raise NotImplementedError(f'method: "{method}" is not supported')
    async with ClientSession(json_serialize=ujson.dumps) as session:
        async with getattr(session, method)(
                await _concat(url), json=await _serialize(body), params=params, headers=headers, data=data
        ) as response:
            try:
                if deserialize:
                    return await _deserialize(await response.json())
                return await response.json()
            except Exception as error:
                return error


async def get(url: str, **kwargs) -> JsonProcessed:
    return await request('get', url, **kwargs)


async def post(url: str, **kwargs) -> JsonProcessed:
    return await request('post', url, **kwargs)


async def put(url: str, **kwargs) -> JsonProcessed:
    return await request('put', url, **kwargs)


async def delete(url: str, **kwargs) -> JsonProcessed:
    return await request('delete', url, **kwargs)


# @aiocache
async def _concat(url: str):
    if not (base := baseurl) or url.startswith('http'):
        return url
    if (not base.endswith('/') and url.startswith('/')) or (base.endswith('/') and not url.startswith('/')):
        return base + url
    if base.endswith('/') and url.startswith('/'):
        return base[:-1] + url
    return f'{base}/{url}'


# @aiocache
async def _serialize(data: JsonProcessed) -> Any:
    if isinstance(data, dict):
        return {key: await _serialize(value) for key, value in data.items()}
    if isinstance(data, list):
        return [await _serialize(element) for element in data]
    if isinstance(data, (int, float, bool, str)) or data is None:
        return data
    return str(data)


# @aiocache
async def _deserialize(json: Any) -> JsonProcessed:
    # handles dict recursively
    if isinstance(json, dict):
        return {key: await _deserialize(value) for key, value in json.items()}
    # handles list recursively
    if isinstance(json, list):
        return [await _deserialize(value) for value in json]
    # 'ed38fe7a-11e6-4c59-ac31-ef30848e8e83' to UUID('ed38fe7a-11e6-4c59-ac31-ef30848e8e83')
    with suppress(Exception):
        return UUID(json)
    from dateutil import parser  # imported inside the function, since package is not built-in
    # '2023-06-09 21:52:49.072155' to datetime.datetime(2023, 6, 9, 21, 52, 49, 72155)
    with suppress(Exception):
        return parser.parse(json)
    # (1, 1.1, True) remains as it is
    if isinstance(json, (int, float, bool)):
        return json
    # "b'bytes'" to b'bytes'
    with suppress(Exception):
        return literal_eval(json)
    # 'string' remains as it is
    if isinstance(json, str):
        return json
    # 'null' to None
    return None
