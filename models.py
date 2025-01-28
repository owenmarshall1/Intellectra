class Movie:
    def __init__(self, movie_id, name, description):
        self.id = movie_id
        self.name = name
        self.description = description
    
    def __str__(self):
        return f"{self.id}: {self.name} - {self.description}"