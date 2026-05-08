import httpx
import config
import uuid


#NOTE: No async is used here! Everything is sequential!
#      In practice, it would be better to use async, but for this example client I don't


def create_movie(name:str, description:str):
    """Handles given information and sends HTTP requests to the netmovies-gateway for the creation of a new movie with the given attributes."""
    #reference to the http client connected (the gateway)
    with httpx.Client(timeout=30.0) as client:
        
        #the HTTP POST given to the netmovies-api to store
        metadata_response = client.post(
            f"{config.GATEWAY_URL}/metadata/movie/createMovie",
            json = {"name" : name, "description": description}
        )
        metadata_response.raise_for_status()
        

        #the new movie that is returned after "we" create it
        new_movie = metadata_response.json()

        #the HTTP POST given to the netmovies-storage to create a directory for a new movie
        storage_response = client.post(
            f"{config.GATEWAY_URL}/storage/movies",
            #using the metadata response to send a new request to the netmovies-storage
            json = {"storage_id": new_movie["storageId"]}
        )

        exit_response = storage_response.raise_for_status()

    return exit_response
    


def get_all_movies():
    """Gets and returns a list of all movies within the netmovies-api database."""

    with httpx.Client() as client:

        #the request
        metadata_response = client.get(
            f"{config.GATEWAY_URL}/metadata/movie/getAllMovies"
        )
        metadata_response.raise_for_status()

        all_movies = metadata_response.json()

    return all_movies
    


def delete_movie_by_storage_id(storage_id:uuid.UUID):

    with httpx.Client() as client:


        metadata_response = client.delete(
            f"{config.GATEWAY_URL}/metadata/movie/deleteMovieByStorageId/{storage_id}"
        )
        metadata_response.raise_for_status()


        storage_response = client.delete(
            f"{config.GATEWAY_URL}/storage/movies/{storage_id}"
        )
        storage_response.raise_for_status()






        


