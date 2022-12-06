import asyncio

from client import Wrapper


async def main():
    client = Wrapper()
    await client.save_doc(True)


asyncio.run(main())
