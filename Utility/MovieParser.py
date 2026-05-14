import aiofiles
import config


async def parse_movie(src: str):
    """Yields movie data in chunks from the given source path."""
    async with aiofiles.open(src, "rb") as file:
        while chunk := await file.read(config.DEFAULT_READ_SIZE):
            yield chunk
