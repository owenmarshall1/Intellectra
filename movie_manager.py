from utils import load_movies, save_movies
from models import Movie

def view_movies():
    movies = load_movies()
    if not movies:
        print("No movies found.")
    else:
        for movie in movies:
            print(movie)
    
def add_movie():
    movies = load_movies()
    movie_id = str(len(movies) + 1)
    name = input("Enter the movie name: ")
    description = input("Enter the movie description: ")

    new_movie = Movie(movie_id, name, description)
    movies.append(new_movie)

    save_movies(movies)
    print(f"Movie '{name}' added successfully.")

def edit_movie():
    movies = load_movies()
    view_movies()
    movie_id = input("Enter the movie ID to edit: ")
    for movie in movies:
        if movie.id == movie_id:
            movie.name = input("Enter the new movie name:")
            movie.description = input("Enter the new movie description:")
            save_movies(movies)
            print(f"Movie '{movie.name}' edited successfully.")
            return

    print("Movie not found.")

def remove_movie():
    movies = load_movies()
    view_movies()
    movie_id = input("Enter the movie ID to remove: ")
    updated_movies = [movie for movie in movies if movie.id != movie_id]
    if len(updated_movies) == len(movies):
        print("Movie not found.")
    else:
        save_movies(updated_movies)
        print("Movie removed successfully.")