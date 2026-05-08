import Client.HTTPHandler as ClientHTTP
import uuid
import config


print(config.GATEWAY_URL)


running = True
while running:

    

    user_input = input(": ")


    if user_input == "create":
        print(ClientHTTP.create_movie(input("Name of new movie: "), input("Description of new movie: ")).json()["status"])


    elif user_input == "list":
        for movie in ClientHTTP.get_all_movies():
            print("--------------------------------------")
            print(f"Movie Name: {movie["name"]}")
            print(f"Description: {movie["description"]}")
            print(f"Storage Id: {movie["storageId"]}")
            print(f"Date Added: {movie["dateAdded"]}")


    elif user_input == "delete":
        uuid_input = input("Storage Id of movie to delete: ")

        try:
            uuid_send = uuid.UUID(uuid_input)
            ClientHTTP.delete_movie_by_storage_id(uuid_send)
        except ValueError as e:
            print(f"UUID provided was not in proper UUID format and is invalid.")
        except Exception as e:
            print(f"An exception was thrown: {e}")


    elif user_input == "quit":
        running = False


    else:
        print("Valid Inputs:\n      'create': Creates a new movie with the given attributes.\n      'quit': Quits NetMovies-Client.\n       'delete': Deletes the movie correlating to the given StorageId.")