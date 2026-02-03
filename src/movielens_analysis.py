import pytest
from collections import Counter
import datetime
import os
import requests  # urllib
import bs4


# ================== class Movies ==================
class Movies:
	"""
	Analyzing data from movies.csv
	"""

	def __init__(self, path_to_the_file):
		self.path_to_the_file = path_to_the_file
		self.data = list(self.read_file())

	def read_file(self):
		"""
		get data from the file
		"""
		with open(self.path_to_the_file, "r", encoding="utf-8") as file:
			header = file.readline().strip().split(",")  # получаем наши заголовки
			lines = list(file)
			for line in lines[:1000]:
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


# ================== class Tags ==================


class Tags:
	"""
	Analyzing data from tags.csv
	"""

	def __init__(self, path_to_the_file):
		"""
		Put here any fields that you think you will need.
		"""
		self.path_to_the_file = path_to_the_file
		self.data = list(self.read_file())

	def read_file(self):
		"""
		get data from the file
		"""
		with open(self.path_to_the_file, "r", encoding="utf-8") as file:
			header = file.readline().strip().split(",")  # получаем наши заголовки
			lines = list(file)
			for line in lines[:1000]:
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


# ================== class Rating ==================
class Ratings:
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
		self.data = list(self.read_file())

	# self.inner_class = self.Movies(self)

	def read_movie(self):
		with open(self.path_to_the_movie_file, "r", encoding="utf-8") as file:
			headers = file.readline().strip().split(",")  # получаем наши заголовки

			movie_id = {}
			lines = list(file)
			for line in lines[:1000]:
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
			lines = list(file)
			for line in lines[:1000]:
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
					for row in self.parent_instance.data
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
				[row["rating"] for row in self.parent_instance.data]
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
				[row[field] for row in self.parent_instance.data if row.get(field)]
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

			for row in self.parent_instance.data:
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

			for row in self.parent_instance.data:
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

		def top_rated_genres(self, n):  # bonus method
			"""
			The method returns top-n genres of the average ratings in the slice of years
			It is a dict where the keys are year and the values are list with genres and their avg ratings.
			Sort it by year and values descendingly.
			The values should be rounded to 2 decimals.
			"""
			sums = {}
			counts = {}

			for row in self.parent_instance.data:
				genres = row.get("genres")
				rating = row.get("rating")
				ts = row.get("timestamp")
				if not genres or rating is None or ts is None:
					continue

				year = datetime.datetime.fromtimestamp(ts).year
				if year not in sums:
					sums[year] = {}
					counts[year] = {}

				for g in genres.split("|"):
					sums[year][g] = sums[year].get(g, 0.0) + float(rating)
					counts[year][g] = counts[year].get(g, 0) + 1

			result = {}
			for year in sorted(sums.keys()):
				avgs = {
					g: round(sums[year][g] / counts[year][g], 2)
					for g in sums[year]
					if counts[year][g] > 0
				}

			top = sorted(avgs.items(), key=lambda x: (x[1], x[0]), reverse=True)[:n]
			result[year] = dict(top)

			return result

	class Users(Movies_rating):
		"""
		In this class, three methods should work.
		The 1st returns the distribution of users by the number of ratings made by them.
		The 2nd returns the distribution of users by average or median ratings made by them.
		The 3rd returns top-n users with the biggest variance of their ratings.
		Inherit from the class Movies. Several methods are similar to the methods from it.
		"""

		group_field = "userId"


# ================== class Links ==================
class Links:
	"""
	Analyzing data from links.csv
	"""

	def __init__(self, path_to_the_link_file, path_to_the_movie_file):
		self.path_to_the_link_file = path_to_the_link_file
		self.path_to_the_movie_file = path_to_the_movie_file
		self.data = self.merge_link_file()

	def merge_link_file(self):
		"""
		get data from the file
		"""
		with open(self.path_to_the_movie_file, "r", encoding="utf-8") as file:
			header = file.readline().strip().split(",")  # получаем заголовки
			movie_data = {}

			lines = list(file)
			for line in lines[:1000]:
				parts = line.strip().split(",")
				title = ",".join(parts[1:-1])
				genres = parts[-1]
				movie_data[parts[0]] = {header[1]: title, header[2]: genres}

		link_data = {}
		with open(self.path_to_the_link_file, "r", encoding="utf-8") as file:
			header = file.readline().strip().split(",")  # получаем заголовки

			lines = list(file)
			for line in lines[:1000]:
				parts = line.strip().split(",")
				info = movie_data.get(parts[0])
				link_data[parts[0]] = {
					header[0]: parts[
						0
					],  # забираем movieId фильма, e.g. https://movielens.org/movies/1
					header[1]: parts[
						1
					],  # забираем imdbId, e.g. http://www.imdb.com/title/tt0114709/
					header[2]: parts[
						-1
					],  # забираем tmdbId, e.g. https://www.themoviedb.org/movie/862
					"title": info["title"] if info else None,
					"genres": info["genres"] if info else None,
				}

		return link_data

	def get_imdb(self, list_of_movies, list_of_fields):
		"""
		The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
		For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
		The values should be parsed from the IMDB webpages of the movies.
		Sort it by movieId descendingly.
		"""

		imdb_info = []

		for id in list_of_movies:
			info = [id]
			imdbId = self.data[f"{id}"]["imdbId"]

			url_themdb = f"https://www.imdb.com/title/tt{imdbId}"
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
			r = requests.get(url_themdb, timeout=10, headers=headers)
			if r.status_code != 200:
				raise requests.HTTPError(
					f"{url_themdb} is not respoding. Got {r.status_code} code"
				)
			soup = bs4.BeautifulSoup(r.text, "html.parser")

			for field in list_of_fields:
				tag = soup.find(string=field)
				if (
						tag is not None
				):  # в некоторых фильмах отсуствует поле Budget, поэтому проверка на отсутствие поля не сработает
					parent = tag.find_parent()
					result = parent.next_sibling()[-1].get_text()
					if "$" in result or "£" in result:
						prepare = result.split()[0]
						info.append(prepare)
					elif "min)" in result:
						prepare = result.lstrip("(").rstrip(")")
						info.append(prepare)
					else:
						info.append(result)
				else:
					info.append(tag)

			imdb_info.append(info)

		return imdb_info

	def top_directors(self, n):
		"""
		The method returns a dict with top-n directors where the keys are directors and
		the values are numbers of movies created by them. Sort it by numbers descendingly.
		"""
		movie_ids = list(self.data.keys())[:75]
		rows = self.get_imdb(movie_ids, ["Director"])
		directors = Counter()
		directors.update([row[1] for row in rows if row[1] is not None])
		directors = dict(directors.most_common(n))

		return directors

	def most_expensive(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are their budgets. Sort it by budgets descendingly.
		"""
		movie_ids = list(self.data.keys())[:75]
		rows = self.get_imdb(movie_ids, ["Budget"])
		budgets = Counter()
		for row in rows:
			if row[1] is not None:
				title = self.data[row[0]]["title"]
				budgets[title] = int(row[1].lstrip("$£").replace(",", ""))
		budgets = dict(budgets.most_common(n))

		return budgets

	def most_profitable(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are the difference between cumulative worldwide gross and budget.
		Sort it by the difference descendingly.
		"""
		movie_ids = list(self.data.keys())[:75]
		rows = self.get_imdb(movie_ids, ["Budget", "Gross worldwide"])
		profits = {}

		for row in rows:
			if row[1] is not None and row[2] is not None:
				title = self.data[row[0]]["title"]
				budget = int(row[1].lstrip("$£").replace(",", ""))
				gross = int(row[2].lstrip("$£").replace(",", ""))
				profits[title] = gross - budget

		profits = dict(sorted(profits.items(), key=lambda x: x[1], reverse=True)[:n])
		return profits

	def longest(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are their runtime. If there are more than one version – choose any.
		Sort it by runtime descendingly.
		"""
		movie_ids = list(self.data.keys())[:75]
		rows = self.get_imdb(movie_ids, ["Runtime"])
		runtimes = Counter()
		for row in rows:
			if row[1] is not None:
				title = self.data[row[0]]["title"]
				runtimes[title] = int(row[1].split()[0])
		runtimes = dict(runtimes.most_common(n))

		return runtimes

	def top_cost_per_minute(self, n):
		"""
		The method returns a dict with top-n movies where the keys are movie titles and
		the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it.
		The values should be rounded to 2 decimals. Sort it by the division descendingly.
		"""
		movie_ids = list(self.data.keys())[:75]
		rows = self.get_imdb(movie_ids, ["Budget", "Runtime"])
		costs = Counter()
		for row in rows:
			if row[1] is not None and row[2] is not None:
				title = self.data[row[0]]["title"]
				budget = int(row[1].lstrip("$£").replace(",", ""))
				runtime = int(row[2].split()[0])
				costs[title] = round(budget / runtime, 2)
		costs = dict(costs.most_common(n))

		return costs

	def top_creative_countries(self, n):  # bonus method
		"""
		The method returns a dict with top-n Countries where the keys are country titles and
		the values are the counts of country of origin movie.
		Sort it by the counts descendingly.
		"""
		movie_ids = list(self.data.keys())[:75]
		rows = self.get_imdb(movie_ids, ["Country of origin"])
		countries = Counter()
		countries.update(row[1] for row in rows if row[1] is not None)
		countries = dict(countries.most_common(n))

		return countries


# lnk = Movies("ml-latest-small/movies.csv")
# print(lnk.dist_by_genres())


# ================== class Test ==================
class Testing:
	class Test_Movies:
		@pytest.fixture(autouse=True)
		def setup(self):
			self.mov = Movies("ml-latest-small/movies.csv")

		# os.path.join(os.path.dirname(__file__), "ml-latest-small/movies.csv")
		# )

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
				assert "movieId" in elem
				assert "title" in elem
				assert "genres" in elem

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
			self.tag = Tags(
				os.path.join(os.path.dirname(__file__), "ml-latest-small/tags.csv")
			)

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
				assert "userId" in elem
				assert "movieId" in elem
				assert "tag" in elem
				assert "timestamp" in elem

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
			word = "funny"
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
				os.path.join(os.path.dirname(__file__), "ml-latest-small/movies.csv"),
			)

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
				assert "userId" in elem
				assert "movieId" in elem
				assert "rating" in elem
				assert "timestamp" in elem

	class Test_Movies_rating:
		@pytest.fixture(autouse=True)
		def setup(self):
			self.rat = Ratings(
				os.path.join(os.path.dirname(__file__), "ml-latest-small/ratings.csv"),
				os.path.join(os.path.dirname(__file__), "ml-latest-small/movies.csv"),
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

	class Test_Links:
		@pytest.fixture(autouse=True)
		def setup(self):
			self.link = Links("ml-latest-small/links.csv", "ml-latest-small/movies.csv")

		def link_check_dct(self, result):
			assert isinstance(result, dict)
			for key, value in result.items():
				assert isinstance(key, str)
				assert isinstance(value, int)
			assert list(result.values()) == sorted(result.values(), reverse=True)

		def test_merge_link_file(self):
			result = self.link.merge_link_file()
			assert isinstance(result, dict)
			for key, value in result.items():
				assert isinstance(key, str)
				assert isinstance(value, dict)
			for elem in result.values():
				assert "movieId" in elem
				assert "imdbId" in elem
				assert "tmdbId" in elem

		def test_get_imdb(self):
			self.list_of_movies = ["1", "2", "3", "4", "5"]

			res = self.link.get_imdb(self.list_of_movies,
									 ["Director", "Runtime", "Budget", "Cumulative Worldwide Gross"])
			assert isinstance(res, list)
			assert isinstance(res[0], list)
			assert len(res[0]) == 5
			assert len(res) == 5

		def test_top_directors(self):
			self.link.data = {}
			self.link.list_of_movies = ["1", "2", "3"]
			n = 2
			result = self.link.top_directors(n)
			# print(result)
			assert isinstance(result, dict)
			assert list(result.values()) == sorted(result.values(), reverse=True)

		def test_most_expensive(self):
			n = 2
			result = self.link.most_expensive(n)
			print(result)
			self.link_check_dct(result)

		def test_most_profitable(self):
			n = 2
			result = self.link.most_profitable(n)
			# print(result)
			assert isinstance(result, dict)
			assert list(result) == sorted(result, key=lambda x: x[1], reverse=True)
			for value in result.values():
				assert isinstance(value, int)

		def test_longest(self):
			n = 5
			result = self.link.longest(n)
			for value in result.values():
				assert isinstance(value, int)
			# print(list(result.values()), sorted(result.values(), reverse=True))
			assert list(result.values()) == sorted(list(result.values()), reverse=True)

		def test_top_cost_per_minute(self):
			n = 3
			result = self.link.top_cost_per_minute(n)
			# print(result)
			assert isinstance(result, dict)
			for value in result.values():
				assert isinstance(value, float)
			assert list(result.values()) == sorted(result.values(), reverse=True)

		def test_top_creative_countries(self):
			n = 3
			result = self.link.top_creative_countries(n)
			# print(result)
			assert isinstance(result, dict)
			self.link_check_dct(result)
