def read_file(path: str, year: int = 0):
    with open(path, 'r', encoding='utf-8') as csv_file:
        csv_lines = csv_file.readlines()
        filtered_lines = []
        for line in csv_lines[1:]:
            temp_line = line.strip().split(';')
            if int(temp_line[6]) >= year:
                filtered_lines.append(temp_line)
    return filtered_lines

def top_n(data: list, genre: str='', n:int=0):
    genres = genre.strip().split(',')
    genre_filter = []
    if len(genres) > 0:
        for film in data:
            for entry in genres:
                if entry in film[2]:
                    genre_filter.append(film)
                    break
    else:
        genre_filter = data
    actors = {}
    for film in data:
        for actor in film[5].split(', '):
            if actor in actors:
                if actors[actor] < float(film[8]):
                    actors[actor] = float(film[8])
            else:
                actors[actor] = float(film[8])
    film_tuples = []
    for film in genre_filter:
        actor_scores = []
        for actor in film[5].split(', '):
            actor_scores.append(actors[actor])
        actor_average = sum(actor_scores) / len(actor_scores)
        film_tuples.append((film[1], film[8], actor_average))
    def sort_alphabetically(tup):
        return tup[0]
    sorted_films = sorted(film_tuples, key = sort_alphabetically)
    def sort_average(tup):
        return (float(tup[1]) + tup[2]) / 2
    true_sort = sorted(sorted_films, key = sort_average, reverse = True)
    ranged_movies = []
    for index in range(n):
        if index < len(true_sort):
            ranged_movies.append((true_sort[index][0], round((float(true_sort[index][1]) + true_sort[index][2]) / 2, 1)))
        else:
            break
    return ranged_movies

def write_file(top: list, file_name: str):
    with open(file_name, 'w') as output_file:
        for t in top:
            output_file.write(t[0] + ', ' + str(t[1]) + '\n')
