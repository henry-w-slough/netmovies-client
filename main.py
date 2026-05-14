import Client.HTTPHandler as ClientHTTP
import uuid
import asyncio


async def main():
    running = True
    while running:
        
        user_input = input(": ")


        if user_input == "create":
            print(await ClientHTTP.create_movie(input("Name of movie: "), input("Description of movie (Optional): "), input("Path of file source: ")))

        elif user_input == "delete":

            try:
                print(await ClientHTTP.delete_movie_by_storage_id(uuid.UUID(input("Storage ID of movie: "))))
            except ValueError:
                print("The given Storage ID is not in proper UUID format.")

        elif user_input == "list":
            all_movies = await ClientHTTP.get_all_movies()

            if all_movies == []:
                print("No movies have been stored within database.")

            elif all_movies != None:
                for movie in all_movies:
                    print("--------------------")
                    print(f"Name: {movie["name"]}")
                    print(f"Description: {movie["description"]}")
                    print(f"Date Added: {movie["dateAdded"]}")
                    print(f"Storage ID: {movie["storageId"]}")

        else:
            print("Valid Inputs:\n    'create': Creates a movie with the given properties.\n    'delete': Deletes a Movie with the given Storage Id.\n    'list': Lists all stored movies.")




if __name__ == "__main__":
    asyncio.run(main())