import httpx
import config
import uuid


def create_movie(name: str, description: str):
    with httpx.Client(timeout=30.0) as client:
        metadata_response = send_request(client.post,
            f"{config.GATEWAY_URL}/metadata/movie/createMovie",
            json={"name": name, "description": description}
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


def get_all_movies():
    with httpx.Client() as client:
        metadata_response = send_request(client.get,
            f"{config.GATEWAY_URL}/metadata/movie/getAllMovies"
        )
        if metadata_response is None:
            return {}
        return metadata_response.json()


def delete_movie_by_storage_id(storage_id: uuid.UUID):
    with httpx.Client() as client:
        send_request(client.delete,
            f"{config.GATEWAY_URL}/metadata/movie/deleteMovieByStorageId/{storage_id}"
        )
        send_request(client.delete,
            f"{config.GATEWAY_URL}/storage/movies/{storage_id}"
        )


def send_request(request, *args, **kwargs) -> httpx.Response | None:
    """Sends the given request and handles errors from the Response."""
    try:
        response = request(*args, **kwargs)
        response.raise_for_status()
        return response
    except httpx.ConnectTimeout:
        print("Gateway timed out connecting.")
    except httpx.ReadTimeout:
        print("Gateway took too long to respond.")
    except httpx.ConnectError:
        print("Could not reach gateway.")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code}: {e.response.json()}")
    return None





        


