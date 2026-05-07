import Client.HTTPHandler as ClientHTTP





running = True
while running:

    user_input = input(": ")

    if user_input == "create":
        ClientHTTP.create_movie(input("Name of new movie: "), input("Description of new movie: "))
        continue
    elif user_input == "quit":
        running = False
        continue
    else:
        print("Valid Inputs:\n      'create': Creates a new movie with the given attributes.\n      'quit': Quits NetMovies-Client.")