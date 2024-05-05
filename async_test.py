import asyncio

async def hello(n):
    print(f"Hello {n}")
    await asyncio.sleep(n)
    print(f"World {n}")
    return n

async def main():
    output = await asyncio.gather(hello(2), hello(1), hello(3))
    return output

if __name__ == "__main__":
    x = asyncio.run(main())
    print(x)