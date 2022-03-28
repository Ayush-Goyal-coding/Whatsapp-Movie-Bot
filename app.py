from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from MovieInfo.movie_rate import get_movie_info,get_body
from MovieInfo.pirate_bay_url import get_msg_with_piratebay_url,get_unblocked_urls_for_pirate_bay
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/pirate_bay_url/all")
def pirate_bay_urls():
    return {"urls": get_unblocked_urls_for_pirate_bay()}


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""

    # Fetch the message
    msg = request.form.get('Body')
    print(request)

    # Create reply
    resp = MessagingResponse()

    greetings = ['hello', 'hi', 'good']
    msg = msg.lower()
    if any(i in msg for i in greetings):
        msg = "Hi, Type the name of the movie you want to search 😁"
        respMsg = resp.message(msg)
        return str(resp)
    else:
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
    resp.message(get_msg_with_piratebay_url(msg))
    return str(resp)


# def translate():


if __name__ == "__main__":
    app.run(debug=True)
