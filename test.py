import asyncio

async def distribute():
    for task in [asyncio.create_task(process(i)) for i in range(2)]:
        await task

async def process(num):
    await operate(num)

async def operate(num):
    while True:
        print(num, " is running")
        await asyncio.sleep(1)

async def main():
    await distribute()

asyncio.run(main())
