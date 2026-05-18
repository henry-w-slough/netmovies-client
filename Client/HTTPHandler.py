import httpx
import config
import uuid
import os
import Utility.MovieParser as MovieParser
import json


async def create_movie(name: str, description: str, src:str) -> dict | None:
    
    async with httpx.AsyncClient() as client:
        
        metadata_response = await send_request(
            client.post,
            f"{config.GATEWAY_ADDRESS}/metadata/movie/createMovie",
            json={"name": name, "description": description}
        )

        if metadata_response == None:
            return None

        new_movie = metadata_response.json()

        storage_directory_response = await send_request(
            client.post,
            f"{config.GATEWAY_ADDRESS}/storage/directory/createMovie/{new_movie["storageId"]}"
        )

        if storage_directory_response == None:
            return None
        
        storage_data_response = await send_request(
            client.post,
            f"{config.STORAGE_ADDRESS}/storage/data/uploadMovieData/"
        )


async def get_all_movies() -> dict | None:

    async with httpx.AsyncClient() as client:
        metadata_response = await send_request(client.get,
            f"{config.GATEWAY_ADDRESS}/metadata/movie/getAllMovies"
        )
        if metadata_response is None:
            return None
    return metadata_response.json()


async def delete_movie_by_storage_id(storage_id: uuid.UUID) -> httpx.Response | None:
    
    async with httpx.AsyncClient() as client:
        return await send_request(client.delete,
            f"{config.GATEWAY_ADDRESS}/metadata/movie/deleteMovieByStorageId/{storage_id}"
        ) and await send_request(client.delete,
            f"{config.GATEWAY_ADDRESS}/data/deleteMovieByStorageId/{storage_id}"
        )


async def send_request(request_func, *args, **kwargs) -> httpx.Response | None:

    try:
        response = await request_func(*args, **kwargs)
        response.raise_for_status()
        return response

    except httpx.ConnectTimeout:
        print(f"Gateway timed out while connection was being established.")
    except httpx.ReadTimeout:
        print("Gateway took too long to respond.")
    except httpx.ConnectError:
        print("Connection with gateway could not be reached.")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error caught:\n    CODE - {e.response.status_code}:\n    DETAIL - {e.response.text}")
    except httpx.RequestError as e:
        print(f"An unexpected error occurred while requesting: {e}")

    return None





        


