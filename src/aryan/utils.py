import inspect


async def async_(obj):
    return (await obj) if inspect.isawaitable(obj) else obj
