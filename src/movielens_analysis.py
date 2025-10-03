<<<<<<< HEAD
import pytest

=======
>>>>>>> 5a793647d33460ae6a28df00fc9d098f05cb01a7
from collections import Counter
import sys
import datetime
import os
import requests  # urllib
import bs4
import json


# ================== class Movies ==================
class Movies:
<<<<<<< HEAD
	"""
	Analyzing data from movies.csv
	"""

	def __init__(self, path_to_the_file):
		self.path_to_the_file = path_to_the_file
		self.data = self.read_file

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

		for line in self.data():  # пробегаемся по нашему генератору
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
		for line in self.data():  # пробегаемся по нашему генератору
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
		for line in self.data():  # пробегаемся по нашему генератору
			movie = line["title"]  # название фильма
			num_genres = len(line["genres"].split("|"))  # кол-во жанров
			movies[movie] = num_genres  # добавялем в counter жанр
		return dict(movies.most_common(n))
=======
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file):
        self.path_to_the_file = path_to_the_file
        self.data = self.read_file

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

        for line in self.data():  # пробегаемся по нашему генератору
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
        for line in self.data():  # пробегаемся по нашему генератору
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
        for line in self.data():  # пробегаемся по нашему генератору
            movie = line["title"]  # название фильма
            num_genres = len(line["genres"].split("|"))  # кол-во жанров
            movies[movie] = num_genres  # добавялем в counter жанр
        return dict(movies.most_common(n))
>>>>>>> 5a793647d33460ae6a28df00fc9d098f05cb01a7


# ================== class Tags ==================


class Tags:
<<<<<<< HEAD
	"""
	Analyzing data from tags.csv
	"""

	def __init__(self, path_to_the_file):
		"""
		Put here any fields that you think you will need.
		"""
		self.path_to_the_file = path_to_the_file
		self.data = self.read_file

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
		for row in self.data():
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
		for row in self.data():
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
		for row in self.data():
			tags_words[row["tag"]] = len(
				list(
					filter(
						lambda item: any(char.isalpha() for char in item),
						row["tag"].split(),
					)
				)  # проверка на слова (минуем цифры и знаки препинания, например тире, дефис и прочее)
			)

		tags_chars = Counter()
		for row in self.data():
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
		popular_tags = Counter([row["tag"] for row in self.data()])
		popular_tags = dict(popular_tags.most_common(n))

		return popular_tags

	def tags_with(self, word):
		"""
		The method returns all unique tags that include the word given as the argument.
		Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
		"""
		words_in_tags = {}
		for row in self.data():
			if row["tag"] not in words_in_tags:
				words_in_tags[row["tag"]] = row["tag"].split()

		tags_with_word = sorted(
			[tag for tag, words in words_in_tags.items() if word in words]
		)

		return tags_with_word
=======
    """
    Analyzing data from tags.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        self.path_to_the_file = path_to_the_file
        self.data = self.read_file

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
        for row in self.data():
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
        for row in self.data():
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
        for row in self.data():
            tags_words[row["tag"]] = len(
                list(
                    filter(
                        lambda item: any(char.isalpha() for char in item),
                        row["tag"].split(),
                    )
                )  # проверка на слова (минуем цифры и знаки препинания, например тире, дефис и прочее)
            )

        tags_chars = Counter()
        for row in self.data():
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
        popular_tags = Counter([row["tag"] for row in self.data()])
        popular_tags = dict(popular_tags.most_common(n))

        return popular_tags

    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        words_in_tags = {}
        for row in self.data():
            if row["tag"] not in words_in_tags:
                words_in_tags[row["tag"]] = row["tag"].split()

        tags_with_word = sorted(
            [tag for tag, words in words_in_tags.items() if word in words]
        )

        return tags_with_word
>>>>>>> 5a793647d33460ae6a28df00fc9d098f05cb01a7


# ================== class Rating ==================
class Ratings:
<<<<<<< HEAD
	"""
	Analyzing data from ratings.csv
	"""

	def __init__(self, path_to_the_rating_file, path_to_the_movie_file):
		"""
		Put here any fields that you think you will need.
		"""
		self.path_to_the_rating_file = path_to_the_rating_file
		self.path_to_the_movie_file = path_to_the_movie_file
		self.movie_data = self.read_movie()
		self.data = self.read_file
		# self.inner_class = self.Movies(self)

	def read_movie(self):
		with open(self.path_to_the_movie_file, "r", encoding="utf-8") as file:
			headers = file.readline().strip().split(",")  # получаем наши заголовки

			movie_id = {}
			for line in file:
				parts = line.strip().split(
					","
				)  # разбиваем наш файл на части по заголовкам

				movie_id[parts[0]] = {
					headers[1]: ",".join(parts[1:-1]),
					headers[2]: parts[-1],
				}

		return movie_id

	def read_file(self):
		"""
		get data from the file
		"""

		with open(self.path_to_the_rating_file, "r", encoding="utf-8") as file:
			header = file.readline().strip().split(",")  # получаем наши заголовки
			movie_info = self.movie_data
			for line in file:
				parts = line.strip().split(
					","
				)  # разбиваем наш файл на части по заголовкам
				info = movie_info.get(parts[1])
				yield {
					header[0]: parts[0],  # забираем userId
					header[1]: parts[1],  # забираем movieId
					header[2]: parts[2],  # забираем rating
					header[3]: int(parts[3]),  # забираем timestamp
					"title": info["title"] if info else None,
					"genres": info["genres"] if info else None,
				}

	class Movies_rating:
		group_field = "title"

		def __init__(self, parent_instance):
			self.parent_instance = parent_instance  # это нужно для получения доступа к свойствам внешнего класса

		def dist_by_year(self):
			"""
			The method returns a dict where the keys are years and the values are counts.
			Sort it by years ascendingly. You need to extract years from timestamps.
			"""
			ratings_by_year = Counter(
				[
					datetime.datetime.fromtimestamp(row["timestamp"]).year
					for row in self.parent_instance.data()
				]
			)
			ratings_by_year = sorted(ratings_by_year.items(), key=lambda pair: pair[1])
			return dict(ratings_by_year)

		def dist_by_rating(self):
			"""
			The method returns a dict where the keys are ratings and the values are counts.
			Sort it by ratings ascendingly.
			"""

			ratings_distribution = Counter()
			ratings_distribution.update(
				[row["rating"] for row in self.parent_instance.data()]
			)
			ratings_distribution = sorted(
				ratings_distribution.items(), key=lambda pair: pair[1]
			)

			return dict(ratings_distribution)

		def top_by_num_of_ratings(self, n):
			"""
			The method returns top-n movies by the number of ratings.
			It is a dict where the keys are movie titles and the values are numbers.
			Sort it by numbers descendingly.
			"""
			field = self.group_field
			top_movies = Counter()
			top_movies.update(
				[row[field] for row in self.parent_instance.data() if row.get(field)]
			)

			top_movies = dict(top_movies.most_common(n))
			return top_movies

		def top_by_ratings(self, n, metric="average"):
			"""
			The method returns top-n movies by the average or median of the ratings.
			It is a dict where the keys are movie titles and the values are metric values.
			Sort it by metric descendingly.
			The values should be rounded to 2 decimals.
			"""
			field = self.group_field
			top_movies_calculations = {}
			top_movies = {}

			for row in self.parent_instance.data():
				if row[field] is not None and row[field] not in top_movies_calculations:
					top_movies_calculations[row[field]] = {
						"rl": [float(row["rating"])],
					}
				elif row[field] in top_movies_calculations:
					top_movies_calculations[row[field]]["rl"].append(
						float(row["rating"])
					)

			if metric == "average":
				for title, values in top_movies_calculations.items():
					top_movies[title] = round(sum(values["rl"]) / len(values["rl"]), 2)
			elif metric == "median":
				for title, values in top_movies_calculations.items():
					middle = len(values["rl"]) // 2
					values["rl"].sort()
					if len(values["rl"]) % 2 == 0:
						top_movies[title] = round(
							(values["rl"][middle - 1] + values["rl"][middle]) / 2, 2
						)
					else:
						top_movies[title] = values["rl"][middle // 2]
			else:
				raise AttributeError("Unknown metric. Available - average, median.")

			top_movies = dict(
				sorted(top_movies.items(), key=lambda x: (x[1], x[0]), reverse=True)[:n]
			)
			return top_movies

		def top_controversial(self, n):
			"""
			The method returns top-n movies by the variance of the ratings.
			It is a dict where the keys are movie titles and the values are the variances.
			Sort it by variance descendingly.
			The values should be rounded to 2 decimals.
			"""
			field = self.group_field
			top_movies_calculations = {}
			top_movies = {}

			for row in self.parent_instance.data():
				if row[field] is not None and row[field] not in top_movies_calculations:
					top_movies_calculations[row[field]] = {
						"rl": [float(row["rating"])],
					}
				elif row[field] in top_movies_calculations:
					top_movies_calculations[row[field]]["rl"].append(
						float(row["rating"])
					)

			for title, ratings in top_movies_calculations.items():
				mean_ratings = sum(ratings["rl"]) / len(ratings["rl"])
				top_movies[title] = round(
					sum((rate - mean_ratings) ** 2 for rate in ratings["rl"])
					/ len(ratings["rl"]),
					2,
				)

			top_movies = dict(
				sorted(top_movies.items(), key=lambda x: (x[1], x[0]), reverse=True)[:n]
			)
			return top_movies

	class Users(Movies_rating):
		"""
		In this class, three methods should work.
		The 1st returns the distribution of users by the number of ratings made by them.
		The 2nd returns the distribution of users by average or median ratings made by them.
		The 3rd returns top-n users with the biggest variance of their ratings.
		Inherit from the class Movies. Several methods are similar to the methods from it.
		"""

		group_field = "userId"


mov = Movies('ml-latest-small/movies.csv')
mov_most_word = mov.dist_by_genres()
print(mov_most_word)


class Testing:
	class Test_Movies:
		@pytest.fixture(autouse=True)
		def setup(self):
			self.mov = Movies(os.path.join(os.path.dirname(__file__), "ml-latest-small/movies.csv"))

		def mov_check_dct(self, result):
			assert isinstance(result, dict)
			for key, value in result.items():
				assert isinstance(key, str)
				assert isinstance(value, int)
			assert list(result.values()) == sorted(result.values(), reverse=True)

		def test_read_file(self):
			result = self.mov.read_file()
			assert isinstance(result, object)
			for elem in list(result):
				assert 'movieId' in elem
				assert 'title' in elem
				assert 'genres' in elem

		def test_dist_by_release(self):
			result = self.mov.dist_by_release()
			self.mov_check_dct(result)

		def test_dist_by_genres(self):
			result = self.mov.dist_by_genres()
			# print(result)
			self.mov_check_dct(result)

		def test_most_genres(self):
			n = 5
			result = self.mov.most_genres(n)
			# print(result)
			self.mov_check_dct(result)

	class Test_Tags:
		@pytest.fixture(autouse=True)
		def setup(self):
			self.tag = Tags(os.path.join(os.path.dirname(__file__), "ml-latest-small/tags.csv"))

		def tag_check_dct(self, result):
			assert isinstance(result, dict)
			for key, value in result.items():
				assert isinstance(key, str)
				assert isinstance(value, int)
			assert list(result.values()) == sorted(result.values(), reverse=True)

		def test_read_file(self):
			result = self.tag.read_file()
			assert isinstance(result, object)
			for elem in list(result):
				assert 'userId' in elem
				assert 'movieId' in elem
				assert 'tag' in elem
				assert 'timestamp' in elem

		def test_most_words(self):
			n = 5
			result = self.tag.most_words(n)
			self.tag_check_dct(result)

		def test_longest(self):
			n = 5
			result = self.tag.longest(n)
			# print(result)
			assert isinstance(result, list)
			for key in result:
				assert isinstance(key, str)

			sp = [len(i) for i in result]
			# print(sp, sorted(sp, reverse=True))
			assert sp == sorted(sp, reverse=True)

		def test_most_words_and_longest(self):
			n = 5
			result = self.tag.most_words_and_longest(n)
			assert isinstance(result, list)
			for key in result:
				assert isinstance(key, str)
			for elem in result:
				assert elem in self.tag.most_words(n) and elem in self.tag.longest(n)

		def test_most_popular(self):
			n = 4
			result = self.tag.most_popular(n)
			self.tag_check_dct(result)

		def test_tags_with(self):
			word = 'funny'
			result = self.tag.tags_with(word)
			assert isinstance(result, list)
			for key in result:
				assert isinstance(key, str)
			# print(result)
			assert result == sorted(result)

	class Test_Ratings:
		@pytest.fixture(autouse=True)
		def setup(self):
			self.rat = Ratings(
				os.path.join(os.path.dirname(__file__), "ml-latest-small/ratings.csv"),
				os.path.join(os.path.dirname(__file__), "ml-latest-small/movies.csv")
			)

		def rat_check_dct(self, result):
			assert isinstance(result, dict)
			for key, value in result.items():
				assert isinstance(key, str)
				assert isinstance(value, int)
			assert list(result.values()) == sorted(result.values(), reverse=True)

		def test_read_movie(self):
			result = self.rat.read_movie()
			# print(result)
			for key, value in result.items():
				assert isinstance(key, str)
				assert isinstance(value, dict)
			assert isinstance(result, dict)

		def test_read_file(self):
			result = self.rat.read_file()
			assert isinstance(result, object)
			for elem in list(result):
				assert 'userId' in elem
				assert 'movieId' in elem
				assert 'rating' in elem
				assert 'timestamp' in elem

	class Test_Movies_rating:
		@pytest.fixture(autouse=True)
		def setup(self):
			self.rat = Ratings(
				os.path.join(os.path.dirname(__file__), "ml-latest-small/ratings.csv"),
				os.path.join(os.path.dirname(__file__), "ml-latest-small/movies.csv")
			)

			self.mov_rat = self.rat.Movies_rating(self.rat)

		def test_dist_by_year(self):
			result = self.mov_rat.dist_by_year()
			for key, value in result.items():
				assert isinstance(key, int)
				assert isinstance(value, int)
			assert isinstance(result, dict)
			assert list(result.values()) == sorted(result.values())

		def test_dist_by_rating(self):
			result = self.mov_rat.dist_by_rating()
			for key, value in result.items():
				assert isinstance(key, str)
				assert isinstance(value, int)
			assert isinstance(result, dict)
			assert list(result.values()) == sorted(result.values())

		def test_top_by_num_of_ratings(self):
			n = 5
			result = self.mov_rat.top_by_num_of_ratings(n)
			assert len(result) == n
			for key, value in result.items():
				assert isinstance(key, str)
				assert isinstance(value, int)
			assert isinstance(result, dict)
			assert list(result.values()) == sorted(result.values(), reverse=True)

		def test_top_by_ratings(self):
			n = 5
			result = self.mov_rat.top_by_ratings(n)
			assert len(result) == n
			for key, value in result.items():
				assert isinstance(key, str)
				assert isinstance(value, float)
			assert isinstance(result, dict)
			assert list(result.values()) == sorted(result.values(), reverse=True)

		def test_top_controversial(self):
			n = 5
			result = self.mov_rat.top_controversial(n)
			assert len(result) == n
			for key, value in result.items():
				assert isinstance(key, str)
				assert isinstance(value, float)
			assert isinstance(result, dict)
			assert list(result.values()) == sorted(result.values(), reverse=True)



=======
    """
    Analyzing data from ratings.csv
    """

    def __init__(self, path_to_the_rating_file, path_to_the_movie_file):
        """
        Put here any fields that you think you will need.
        """
        self.path_to_the_rating_file = path_to_the_rating_file
        self.path_to_the_movie_file = path_to_the_movie_file
        self.movie_data = self.read_movie()
        self.data = self.read_file
        # self.inner_class = self.Movies(self)

    def read_movie(self):
        with open(self.path_to_the_movie_file, "r", encoding="utf-8") as file:
            headers = file.readline().strip().split(",")  # получаем наши заголовки

            movie_id = {}
            for line in file:
                parts = line.strip().split(
                    ","
                )  # разбиваем наш файл на части по заголовкам

                movie_id[parts[0]] = {
                    headers[1]: ",".join(parts[1:-1]),
                    headers[2]: parts[-1],
                }

        return movie_id

    def read_file(self):
        """
        get data from the file
        """

        with open(self.path_to_the_rating_file, "r", encoding="utf-8") as file:
            header = file.readline().strip().split(",")  # получаем наши заголовки
            movie_info = self.movie_data
            for line in file:
                parts = line.strip().split(
                    ","
                )  # разбиваем наш файл на части по заголовкам
                info = movie_info.get(parts[1])
                yield {
                    header[0]: parts[0],  # забираем userId
                    header[1]: parts[1],  # забираем movieId
                    header[2]: parts[2],  # забираем rating
                    header[3]: int(parts[3]),  # забираем timestamp
                    "title": info["title"] if info else None,
                    "genres": info["genres"] if info else None,
                }

    class Movies_rating:
        group_field = "title"

        def __init__(self, parent_instance):
            self.parent_instance = parent_instance  # это нужно для получения доступа к свойствам внешнего класса

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts.
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            ratings_by_year = Counter(
                [
                    datetime.datetime.fromtimestamp(row["timestamp"]).year
                    for row in self.parent_instance.data()
                ]
            )
            ratings_by_year = sorted(ratings_by_year.items(), key=lambda pair: pair[1])
            return dict(ratings_by_year)

        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sort it by ratings ascendingly.
            """

            ratings_distribution = Counter()
            ratings_distribution.update(
                [row["rating"] for row in self.parent_instance.data()]
            )
            ratings_distribution = sorted(
                ratings_distribution.items(), key=lambda pair: pair[1]
            )

            return dict(ratings_distribution)

        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings.
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """
            field = self.group_field
            top_movies = Counter()
            top_movies.update(
                [row[field] for row in self.parent_instance.data() if row.get(field)]
            )

            top_movies = dict(top_movies.most_common(n))
            return top_movies

        def top_by_ratings(self, n, metric="average"):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            field = self.group_field
            top_movies_calculations = {}
            top_movies = {}

            for row in self.parent_instance.data():
                if row[field] is not None and row[field] not in top_movies_calculations:
                    top_movies_calculations[row[field]] = {
                        "rl": [float(row["rating"])],
                    }
                elif row[field] in top_movies_calculations:
                    top_movies_calculations[row[field]]["rl"].append(
                        float(row["rating"])
                    )

            if metric == "average":
                for title, values in top_movies_calculations.items():
                    top_movies[title] = round(sum(values["rl"]) / len(values["rl"]), 2)
            elif metric == "median":
                for title, values in top_movies_calculations.items():
                    middle = len(values["rl"]) // 2
                    values["rl"].sort()
                    if len(values["rl"]) % 2 == 0:
                        top_movies[title] = round(
                            (values["rl"][middle - 1] + values["rl"][middle]) / 2, 2
                        )
                    else:
                        top_movies[title] = values["rl"][middle // 2]
            else:
                raise AttributeError("Unknown metric. Available - average, median.")

            top_movies = dict(
                sorted(top_movies.items(), key=lambda x: (x[1], x[0]), reverse=True)[:n]
            )
            return top_movies

        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
            Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            field = self.group_field
            top_movies_calculations = {}
            top_movies = {}

            for row in self.parent_instance.data():
                if row[field] is not None and row[field] not in top_movies_calculations:
                    top_movies_calculations[row[field]] = {
                        "rl": [float(row["rating"])],
                    }
                elif row[field] in top_movies_calculations:
                    top_movies_calculations[row[field]]["rl"].append(
                        float(row["rating"])
                    )

            for title, ratings in top_movies_calculations.items():
                mean_ratings = sum(ratings["rl"]) / len(ratings["rl"])
                top_movies[title] = round(
                    sum((rate - mean_ratings) ** 2 for rate in ratings["rl"])
                    / len(ratings["rl"]),
                    2,
                )

            top_movies = dict(
                sorted(top_movies.items(), key=lambda x: (x[1], x[0]), reverse=True)[:n]
            )
            return top_movies

    class Users(Movies_rating):
        """
        In this class, three methods should work.
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
        Inherit from the class Movies. Several methods are similar to the methods from it.
        """

        group_field = "userId"
>>>>>>> 5a793647d33460ae6a28df00fc9d098f05cb01a7
