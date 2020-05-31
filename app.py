from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

BASE_URL = "http://www.omdbapi.com/?t="
API_KEY = "&apikey=751eb215"
PIRATE_BAY_URL = "https://thepiratebay.org/search.php?q="

app = Flask(__name__)


def get_movie_info(title):
    title = title.replace(" ",'+')
    url = BASE_URL+title+API_KEY
    r = requests.get(url)
    return r.json()

def get_ratings(details):
    body = "*Ratings* : \n"
    for i in details['Ratings']:
        body += i['Source'] + " : " + i['Value']+'\n'
    return body

def format_util(x,details):
    return "*"+x+"* : " + details[x] + '\n'

def get_body(title,details):
    if('Error' in details):
        return "Sorry no movie named "+title+" found."
    else:
        body =("Here is your Movie details\n"+
               format_util('Title',details)+
               format_util('Runtime',details)+
               format_util('Genre',details)+
               format_util('Released',details)+
                get_ratings(details)
              )
        
    return body
        
@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    
    # Fetch the message
    msg = request.form.get('Body')
    print(request)



    # Create reply
    resp = MessagingResponse()
    
    greetings = ['hello','hi','good']
    msg = msg.lower()
    if(any(i in msg for i in greetings)):
    	msg = "Hi, Type the name of the movie you want to search 😁"
    	respMsg = resp.message(msg)
    	return str(resp)
    else:
    	title = msg.lower()

    #getting details of movie
    details = get_movie_info(title)
    if('Error' in details):
        body = "Sorry no movie named "+title+" found."
        respMsg = resp.message(body)
        return str(resp)


    body = get_body(title, details)
    imgUrl = details['Poster']

    
    respMsg = resp.message(body)
    respMsg.media(imgUrl)
    resp.message(PIRATE_BAY_URL+msg.replace(" ",'+'))
    return str(resp)

# def translate():


if __name__ == "__main__":
    app.run(debug=True)