from conf.configs import CustomBot, BASE


async def get(url):
    async with CustomBot.SESSION.get(BASE + url) as r:
        return (r, await r.json())


async def post(url, data):
    async with CustomBot.SESSION.post(BASE + url, data=data) as r:
        return (r, await r.json())


async def patch(url, data):
    async with CustomBot.SESSION.patch(BASE + url, data=data) as r:
        return (r, await r.json())

async def delete(url):
    async with CustomBot.SESSION.delete(BASE+url) as r:
        return (r, await r.text())
