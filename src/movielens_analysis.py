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


class Tags:
    """
    Analyzing data from tags.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
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
                    header[0]: parts[0],  # забираем userId
                    header[1]: parts[1],  # забираем movieId
                    header[2]: parts[2],  # забираем tag
                    header[3]: parts[3],  # забираем timestamp
                }

    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        """

        big_tags = Counter()
        for row in self.data:
            big_tags[row["tag"]] = len(
                list(
                    filter(
                        lambda item: any(char.isalpha() for char in item),
                        row["tag"].split(),
                    )
                )  # проверка на слова (минуем цифры и знаки препинания, например тире, дефис и прочее)
            )

        big_tags = dict(big_tags.most_common(n))
        return big_tags

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        big_tags = Counter()
        for row in self.data:
            big_tags[row["tag"]] = len(row["tag"])  # длина тэга = кол-во символов

        big_tags = [tag for tag, _ in big_tags.most_common(n)]
        return big_tags

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        tags_words = Counter()
        for row in self.data:
            tags_words[row["tag"]] = len(
                list(
                    filter(
                        lambda item: any(char.isalpha() for char in item),
                        row["tag"].split(),
                    )
                )  # проверка на слова (минуем цифры и знаки препинания, например тире, дефис и прочее)
            )

        tags_chars = Counter()
        for row in self.data:
            tags_chars[row["tag"]] = len(row["tag"])  # длина тэга = кол-во символов

        big_tags = set(tag for tag, _ in tags_words.most_common(n)) & set(
            tag for tag, _ in tags_chars.most_common(n)
        )
        return list(big_tags)

    def most_popular(self, n):
        """
        The method returns the most popular tags.
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        popular_tags = Counter([row["tag"] for row in self.data])
        popular_tags = dict(popular_tags.most_common(n))

        return popular_tags

    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        words_in_tags = {}
        for row in self.data:
            if row["tag"] not in words_in_tags:
                words_in_tags[row["tag"]] = row["tag"].split()

        tags_with_word = sorted(
            [tag for tag, words in words_in_tags.items() if word in words]
        )

        return tags_with_word
