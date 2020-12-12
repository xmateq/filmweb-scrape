import requests
import jmespath
from bs4 import BeautifulSoup
import re

final_results = []
titles = []
posters = []
rates = []
genres = []
directors = []
results = {}

response = requests.get('https://www.filmweb.pl/serials/search?endRate=10&orderBy=popularity&descending=true&startRate=9')
soup = BeautifulSoup(response.content, 'html.parser')
results_list = soup.find(class_="resultsList hits")

results_list_posters = results_list.find_all(class_='poster__image')
for poster in results_list_posters:
    posters.append(jmespath.search('content', poster))

results_list_titles = results_list.find_all(class_='filmPreview__title')
for title in results_list_titles:
    titles.append(title.get_text())

results_list_rates = results_list.find_all(class_="rateBox__rate")
for rate in results_list_rates:
    rates.append(rate.get_text())

for genre in results_list:
    genre1 = genre.find(class_="filmPreview__info filmPreview__info--genres")
    try:
        genres.append(re.findall('[A-Z][^A-Z]*', genre1.get_text()))
    except:
        genres.append(None)

for director in results_list:
    director1 = director.find(class_="filmPreview__info filmPreview__info--directors")
    try:
        directors.append(director1.get_text().lstrip('twórca'))
    except:
        directors.append(None)

tuples_list = (zip(titles, posters, rates, genres, directors))
keys = ('title', 'poster', 'rate', 'genre', 'director') * 10


def convert(tuple, dic):
    dic = dict(tuple)
    return dic


for ele in tuples_list:
    tuple = list(zip(keys, ele))
    tuple_dict = convert(tuple, results)
    final_results.append(tuple_dict)

print(final_results)
