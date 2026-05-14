import asyncio
import aiofiles
import config

def parse_movie(src:str):

    with open(src, "rb") as f:
        while chunk := f.read(config.DEFAULT_READ_SIZE):
            yield chunk
