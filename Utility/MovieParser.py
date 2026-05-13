import asyncio
import aiofiles

async def parse_movie(src:str):

    async with aiofiles.open(src, "rb") as file:

        while True:
            chunk = await file.read(1024 * 1024) #1MB reads

            if not chunk:
                #EOF
                break

            yield chunk
