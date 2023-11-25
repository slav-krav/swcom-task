import aiohttp
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from settings import OPA_URL


async def _check_permission(method, path, auth_header) -> bool:
    """Makes request to OPA service.
    Configure env var OPA_URL to send request to a proper address"""
    payload = {
        'input':
            {'method': method,
             'path': path,
             'authorization': auth_header}
    }
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.post(f'{OPA_URL}/v1/data/policy', json=payload, headers=headers) as response:
            decision = await response.json()
    return decision['result']['allow']


async def opa_access_check(request: Request, call_next):
    if not await _check_permission(request.method,
                                   request.url.path,
                                   request.headers.get('Authorisation')):
        return JSONResponse({"Error": "403, Policy violation"}, status_code=403)
    return await call_next(request)
