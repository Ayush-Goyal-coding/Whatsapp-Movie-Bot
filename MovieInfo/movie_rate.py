import requests
from twilio.twiml.messaging_response import MessagingResponse
from MovieInfo.pirate_bay_url import get_msg_with_piratebay_url

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


def create_msg_response_for_movie_rating(msg):
    # Create reply
    resp = MessagingResponse()

    title = msg.lower()
    # getting details of movie
    details = get_movie_info(title)
    if 'Error' in details:
        body = "Sorry no movie named " + title + " found."
        respMsg = resp.message(body)
        return str(resp)

    body = get_body(title, details)
    imgUrl = details['Poster']

    respMsg = resp.message(body)
    respMsg.media(imgUrl)
    ## we can parallelise both the messages to improve performance though it is not needed
    resp.message(get_msg_with_piratebay_url(msg))
    return resp