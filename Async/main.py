import asyncio
import time as t

async def fetch_weather():
    print("fetching weather data")
    await asyncio.sleep(4)
    print("fetched weather data")

async def fetch_news():
    print("fetching news data")
    await asyncio.sleep(2)
    print("fetched news data")


async def main():
    start = t.time()
    await asyncio.gather(fetch_weather(), fetch_news())
    end = t.time()
    print(f"Time taken: {end-start}")


if __name__ == "__main__":
    asyncio.run(main())