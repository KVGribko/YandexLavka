from ratelimit.types import Scope


async def all_users_rps(scope: Scope) -> tuple[str, str]:
    return "all_users", "default"
