# Development

## Middleware
For better enhancement of visibility and analysis of requests, we use `logMiddleware` to grant each request an identity(uuid 4) and record time it costs.If you need to use it, try to:`router = APIRouter(route_class=logMiddleware)`on each endpoint
## Response
All the responses  inherit from JSONResponse of fastapi.The member contains http_status_code, code, data and msg.Each response holds its corresponding different member value.When it comes to return a data to frontend, you need to:
```python
from app.core.response import CustomizeApiResponse

@router.get('/')
async def _():
    # user_info
    return CustomizeApiResponse(data=user_info)
```

## Exceptions  
The exceptions are divided into two types, including http exceptions(man-made) and internal exceptions.Both of exceptions are managed by exception_handlers of fastapi.In this way, there is no need to handle errors everywhere.Instead, all you need to do is manage exception_handle function.
When encounerting situations suah as insufficient permissions, use:
```python
if permitted:
    return user_info
else:
    raise HTTPException(status_code=401)
```
instead of:
```python
if permitted:
    return user_info
else:
    return {code: 401, msg: 'no authorization'}
```
The exception_handle will recognize the status_code and return corresponding response class.

## Redis
The specification of redis key should be as as follows:
```
project : business : unique_key

for examples:  smart_hc:throttle:127.0.0.1-user 
```

## Sqlalchemy
1. use `async with async_session.begin() as session` instead of `async with async_sesion() as session`
> These two codes have different functions.They both provide an async context mangager, but the former can automatively commit and rollback.It should be noted that：you should not use `await session.commit()` on `async with async_session.begin() as session)`, use `await session.flush()` instead.
2. if you need to return a sqlalchemy class from the context manager, remember to add `await session.expunge(object)` in the end.
> When the context manager ends, the session will close and then objects of sqlalchemy expire.So that you can **not** retrieve the properties of the returned object later.`expunge_all` or `expunge` function can help keep objects