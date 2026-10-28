from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings

limiter = Limiter(
    key_func = get_remote_address,
    storage_uri = settings.redis_rate_limit_url,
    default_limits = ["60/minute"],
    in_memory_fallback_enabled= True,
    in_memory_fallback = ["60/minute"],
)