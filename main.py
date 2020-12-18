import requests
import jmespath
from bs4 import BeautifulSoup

MOVIES_URL = 'https://www.filmweb.pl/serials/search?endRate=10&orderBy=popularity&descending=true&startRate=9&page={}'
PAGES_TO_GET = 20


def find_movies_of_n_pages(PAGES_TO_GET: int) -> list:

    def find_movies(page: int):
        for _ in range(3):
            response = requests.get(MOVIES_URL.format(page))
            print(response.status_code)
            if response.status_code == requests.codes.ok:
                soup = BeautifulSoup(response.content, 'html.parser')
                films = soup.find(class_="resultsList hits")
                if films:
                    return films
        raise Exception("Invalid response received")

    def get_movie_property_text(movie, classname: str) -> str:
        result = movie.find(class_=classname)
        return result.get_text()

    def find_movie_poster(movie) -> list:
        return jmespath.search('content', movie.find(class_='poster__image'))

    def find_movie_title(movie) -> str:
        return get_movie_property_text(movie, 'filmPreview__title')

    def find_movie_rate(movie) -> str:
        return get_movie_property_text(movie, 'rateBox__rate')

    def find_movie_genre(movie) -> list:
        try:
            return [genre.get_text() for genre in movie.find(class_='filmPreview__info filmPreview__info--genres').find_all('a')]
        except AttributeError:
            return []

    def find_movie_director(movie) -> list:
        try:
            return [director.get_text() for director in movie.find(class_='filmPreview__info filmPreview__info--directors').find_all('a')]
        except AttributeError:
            return []

    def get_movie(movie) -> dict:
        return {
            'title': find_movie_title(movie),
            'poster': find_movie_poster(movie),
            'rate': find_movie_rate(movie),
            'genre': find_movie_genre(movie),
            'director': find_movie_director(movie)
        }

    def final_results(page: int) -> list:
        return [get_movie(movie) for movie in find_movies(page)]

    return [final_results(page) for page in range(1, PAGES_TO_GET+1)]


print(find_movies_of_n_pages(PAGES_TO_GET))
