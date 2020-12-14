import requests
import jmespath
from bs4 import BeautifulSoup
import re


def find_movies():
    response = requests.get('https://www.filmweb.pl/serials/search?endRate=10&orderBy=popularity&descending=true&startRate=9')
    soup = BeautifulSoup(response.content, 'html.parser')
    films = soup.find(class_="resultsList hits")
    return films


def find_movie_poster(movie):
    return jmespath.search('content', movie.find(class_='poster__image'))


def find_movie_title(movie):
    title = movie.find(class_='filmPreview__title')
    return title.get_text()


def find_movie_rate(movie):
    rate = movie.find(class_='rateBox__rate')
    return rate.get_text()


def find_movie_genre(movie):
    try:
        genre = movie.find(class_='filmPreview__info filmPreview__info--genres')
        return re.findall('[A-Z][^A-Z]*', genre.get_text())
    except:
        return "None"


def find_movie_director(movie):
    try:
        director = movie.find(class_='filmPreview__info filmPreview__info--directors')
        return director.get_text().lstrip('twórca')
    except:
        return "None"


def create_dictionaries():
    final = []
    for movie in find_movies():
        result_dic = {
            'title': find_movie_title(movie),
            'poster': find_movie_poster(movie),
            'rate': find_movie_rate(movie),
            'genre': find_movie_genre(movie),
            'director': find_movie_director(movie)
        }
        final.append(result_dic)
    return final

print(create_dictionaries())