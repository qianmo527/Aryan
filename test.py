import asyncio


async def a(num: int):
    while True:
        print(num)
        asyncio.sleep(1)

async def main():
    await asyncio.gather(*[a(num) for num in range(2)])

asyncio.run(main())
