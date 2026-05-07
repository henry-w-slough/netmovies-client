import httpx
import config


#NOTE: No async is used here! Everything is sequential!
#      In practice, it would be better to use async, but for this example client I don't


def create_movie(name:str, description:str):
    """Handles given information and sends HTTP requests to the netmovies-gateway for the creation of a new movie with the given attributes."""
    #reference to the http client connected (the gateway)
    with httpx.Client() as client:
        
        #the HTTP POST given to the netmovies-api to store
        metadata_response = client.post(
            f"{config.GATEWAY_URL}/metadata/movie/createMovie",
            json = {"name" : name, "description": description}
        )
        #auto-checks for metadata response errors
        metadata_response.raise_for_status()
        

        #the new movie that is returned after "we" create it
        new_movie = metadata_response.json()


        #the HTTP POST given to the netmovies-storage to create a directory for a new movie
        storage_response = client.post(
            f"{config.GATEWAY_URL}/storage/movies",
            #using the metadata response to send a new request to the netmovies-storage
            json = {"storage_id": new_movie["storageId"]}
        )
        storage_response.raise_for_status()

        return new_movie
