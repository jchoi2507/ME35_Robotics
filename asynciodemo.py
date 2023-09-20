import asyncio

async def coroutine1():
    print("Coroutine 1 starting...\n")
    await asyncio.sleep(2) # yields processor for 2 seconds
    print("Coroutine 1 ending...\n")

async def coroutine2():
    print("Coroutine 2 starting...\n")
    for i in range(3):
        print(i)
        await asyncio.sleep(0.25) # yields processor for 0.25 seconds
    print("Coroutine 2 ending...\n")

async def main():
    task1 = asyncio.create_task(coroutine1()) # creates and starts task 1
    task2 = asyncio.create_task(coroutine2()) # creates task 2

    await task1
    #await task2

asyncio.run(main())
