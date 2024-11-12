def read_file(pathname: str, year: int = 0):
    movies = []
    with open(pathname, mode='r', encoding='utf-8') as file:
        file.readline()
        for line in file:
            row = line.strip().split(';')
            try:
                movie_year = int(row[6])
                rating = row[8]
                try:
                    rating = float(rating) if rating.replace('.', '', 1).isdigit() else 0.0
                except ValueError:
                    rating = 0.0
                if movie_year >= year:
                    movies.append(row[:6] + [movie_year] + row[7:9] + [rating] + row[9:])
            except ValueError:
                continue
    return movies

def top_n(data, genre='', n=0):
    def get_actor_highest_rating(actor, all_movies):
        max_rating = 0.0
        for movie in all_movies:
            if actor in movie[5]:
                try:
                    rating = float(movie[9])
                    if rating > max_rating:
                        max_rating = rating
                except ValueError:
                    continue
        return max_rating

    genres = [g.strip().lower() for g in genre.split(',')] if genre else []
    filtered_movies = []
    for movie in data:
        movie_genres = movie[2].lower().split(',')
        if not genres or any(g in movie_genres for g in genres):
            filtered_movies.append(movie)

    results = []
    for movie in filtered_movies:
        title = movie[1]
        try:
            rating = float(movie[9])
        except ValueError:
            continue

        actors = movie[5].split(', ')
        actor_ratings = [get_actor_highest_rating(actor, data) for actor in actors]
        actor_rating = sum(actor_ratings) / len(actor_ratings) if actor_ratings else 0

        avg_rating = (rating + actor_rating) / 2
        results.append((title, rating, actor_rating, avg_rating))

    results.sort(key=lambda x: (-x[3], x[0]))
    top_movies = [(title, avg_rating) for title, _, _, avg_rating in results]
    return top_movies[:n] if n > 0 else top_movies

def write_file(top, file_name):
    with open(file_name, mode='w', encoding='utf-8') as file:
        for title, rating in top:
            file.write(f"{title}, {rating:.1f}\n")
