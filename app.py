from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from MovieInfo.movie_rate import create_msg_response_for_movie_rating
from MovieInfo.pirate_bay_url import get_msg_with_piratebay_url,get_unblocked_urls_for_pirate_bay
from AnonymousMailing.send_mail_from_gmail import input_msg_expected, create_msg_response_for_sending_mail
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/pirate_bay_url/all")
def pirate_bay_urls():
    return str({"urls": get_unblocked_urls_for_pirate_bay()})


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message.
    Ref: https://www.twilio.com/docs/sms/tutorials/how-to-receive-and-reply-python
    """

    # Fetch the message
    msg = request.form.get('Body')
    print(request)
    msg = msg.lower()
    print("message recieved: ",msg)


    if msg=="hi" or msg=="hello":
        # Create reply
        resp = MessagingResponse()
        msg = "Hi, Type the name of the movie you want to search 😁 or \n" \
              "Send Anonymous mail by typing the following in the same text \n" \
              + input_msg_expected()
        respMsg = resp.message(msg)
        return str(resp)
    elif "send email" in msg:
        print("inside elif")
        resp = create_msg_response_for_sending_mail(msg)
    else:
        resp = create_msg_response_for_movie_rating(msg)

    return str(resp)


# def translate():


if __name__ == "__main__":
    app.run(debug=False)
