from fastapi import FastAPI, Request, Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import Callable, Union

StrOrCallable = Union[str, Callable[..., str]]


def create_rate_limiter(app: FastAPI, rate_limit_value: StrOrCallable) -> Callable:
    limiter = Limiter(key_func=get_remote_address, headers_enabled=True)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type: ignore[arg-type]

    @limiter.limit(rate_limit_value)
    async def rate_limiter(request: Request, response: Response):
        return None
    
    return rate_limiter

if __name__ == "__main__":
    app = FastAPI()
    rate_limiter = create_rate_limiter(app, "5/10seconds")