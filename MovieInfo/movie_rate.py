import requests

BASE_URL = "http://www.omdbapi.com/?t="
API_KEY = "&apikey=751eb215"

def get_ratings(details):
    body = "*Ratings* : \n"
    for i in details['Ratings']:
        body += i['Source'] + " : " + i['Value'] + '\n'
    return body


def format_util(x, details):
    return "*" + x + "* : " + details[x] + '\n'


def get_body(title, details):
    if 'Error' in details:
        return "Sorry no movie named " + title + " found."
    else:
        body = ("Here is your Movie details\n" +
                format_util('Title', details) +
                format_util('Runtime', details) +
                format_util('Genre', details) +
                format_util('Released', details) +
                get_ratings(details)
                )

    return body


def get_movie_info(title):
    title = title.replace(" ", '+')
    url = BASE_URL + title + API_KEY
    r = requests.get(url)
    return r.json()

