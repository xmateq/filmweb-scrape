import requests
import jmespath
from bs4 import BeautifulSoup

HTTP_SUCCES = 200
MOVIES_URL = 'https://www.filmweb.pl/serials/search?endRate=10&orderBy=popularity&descending=true&startRate=9{}'

try:
    n = int(input("How many pages do you want to scrape?"))
except ValueError:
    raise Exception("Invalid value")


def find_movies_of_n_pages(n=n):

    def find_movies(page):
        response = requests.get(MOVIES_URL.format(f'&page={page}'))
        if response.status_code == HTTP_SUCCES:
            soup = BeautifulSoup(response.content, 'html.parser')
            films = soup.find(class_="resultsList hits")
            if films:
                return films
            else:
                raise Exception("No such an element")
        else:
            raise Exception("Invalid response recived")

    def get_movie_property_text(movie, classname: str) -> str:
        result = movie.find(class_=classname)
        return result.get_text()

    def find_movie_poster(movie):
        return jmespath.search('content', movie.find(class_='poster__image'))

    def find_movie_title(movie):
        return get_movie_property_text(movie, 'filmPreview__title')

    def find_movie_rate(movie):
        return get_movie_property_text(movie, 'rateBox__rate')

    def find_movie_genre(movie):
        try:
            return [genre.get_text() for genre in movie.find(class_='filmPreview__info filmPreview__info--genres').find_all('a')]
        except AttributeError:
            return []

    def find_movie_director(movie):
        try:
            return [director.get_text() for director in movie.find(class_='filmPreview__info filmPreview__info--directors').find_all('a')]
        except AttributeError:
            return []

    def get_movie(movie):
        return {
            'title': find_movie_title(movie),
            'poster': find_movie_poster(movie),
            'rate': find_movie_rate(movie),
            'genre': find_movie_genre(movie),
            'director': find_movie_director(movie)
        }

    def final_results(page):
        return [get_movie(movie) for movie in find_movies(page)]

    return [final_results(page) for page in range(1, n+1)]

print(find_movies_of_n_pages())
