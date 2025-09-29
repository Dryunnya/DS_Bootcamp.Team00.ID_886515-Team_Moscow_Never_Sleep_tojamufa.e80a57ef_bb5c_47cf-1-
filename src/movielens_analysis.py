from collections import Counter


class Movies:
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file):
        self.path_to_the_file = path_to_the_file
        self.data = self.read_file()

    def read_file(self):
        """
        get data from the file
        """
        with open(self.path_to_the_file, "r", encoding="utf-8") as file:
            header = file.readline().strip().split(",")  # получаем наши заголовки
            for line in file:
                parts = line.strip().split(
                    ","
                )  # разбиваем наш файл на части по заголовкам
                yield {
                    header[0]: parts[0],  # забираем id фильма
                    header[1]: ",".join(
                        parts[1:-1]
                    ),  # забираем наименование (title), восстанавливаем, если внутри были запятые
                    header[2]: parts[-1],  # забираем жанр фильма
                }

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts.
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        release_years = Counter()

        for line in self.data:  # пробегаемся по нашему генератору
            year = (
                line["title"].strip().split("(")[-1].strip(")").strip(')"')
            )  # из каждого title вытягиваем год
            if any(char.isalpha() for char in year):  # проверка на фильмы без годов
                release_years["Unknown year"] += 1
                # continue
            else:
                release_years[year] += 1  # добавялем в counter год
        return dict(release_years.most_common())

    def dist_by_genres(self):
        """
           The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        """
        genres = Counter()
        for line in self.data:  # пробегаемся по нашему генератору
            genres_list = line["genres"].split("|")  # из каждого genre вытягиваем жанр
            for genre in genres_list:
                genres[genre] += 1  # добавялем в counter жанр
        return dict(genres.most_common())

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        movies = Counter()
        for line in self.data:  # пробегаемся по нашему генератору
            movie = line["title"]  # название фильма
            num_genres = len(line["genres"].split("|"))  # кол-во жанров
            movies[movie] = num_genres  # добавялем в counter жанр
        return dict(movies.most_common(n))
