import httpx
import config
import uuid
import os


def create_movie(name: str, description: str) -> dict | None:
    
    with httpx.Client() as client:
        
        if len(description) == 0:
            movie_json = {"name": name}
        else:
            movie_json = {"name": name, "description": description}

        metadata_response = send_request(client.post,
            f"{config.GATEWAY_URL}/metadata/movie/createMovie",
            json=movie_json
        )
        if metadata_response is None:
            return None

        new_movie = metadata_response.json()

        storage_response = send_request(client.post,
            f"{config.GATEWAY_URL}/storage/movies",
            json={"storage_id": new_movie["storageId"]}
        )

        if storage_response is None:
            return None

    return new_movie


def get_all_movies() -> dict | None:
    with httpx.Client() as client:
        metadata_response = send_request(client.get,
            f"{config.GATEWAY_URL}/metadata/movie/getAllMovies"
        )
        if metadata_response is None:
            return None
    return metadata_response.json()



def delete_movie_by_storage_id(storage_id: uuid.UUID) -> httpx.Response | None:
    with httpx.Client() as client:
        return send_request(client.delete,
            f"{config.GATEWAY_URL}/metadata/movie/deleteMovieByStorageId/{storage_id}"
        ) and send_request(client.delete,
            f"{config.GATEWAY_URL}/storage/movies/{storage_id}"
        )


def send_request(request_func, *args, **kwargs) -> httpx.Response | None:

    try:
        response = request_func(*args, **kwargs)
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



def send_file(self):
    pass





        


