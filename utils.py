import csv
from models import Movie

CSV_FILE = "data.csv"

def load_movies():
    movies = []
    try:
        with open(CSV_FILE, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                movies.append(Movie(row['id'], row['name'], row['description']))
    except FileNotFoundError:
        print("CSV file not found. Creating a new one.")
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'description'])
    return movies

def save_movies(movies):
    with open(CSV_FILE, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'description'])
        for movie in movies:
            writer.writerow([movie.id, movie.name, movie.description])