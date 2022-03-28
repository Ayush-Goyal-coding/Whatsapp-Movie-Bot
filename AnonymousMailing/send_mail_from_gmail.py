import smtplib
from email.message import EmailMessage
import os
from twilio.twiml.messaging_response import MessagingResponse

FROM_EMAIL = 'bot.by.fun@gmail.com'
pwd = os.environ['GMAIL_APP_PASSWORD_BOT']  ## replace this by your app password

def input_msg_expected()->str:
    '''
    Users are expectetd to send the message in this format
    '''
    msg_format = "*Send email*\n" \
                 "<to>\n" \
                 "<subject>\n" \
                 "<body>"
    return msg_format


def email_alert(subject, body, to):
    '''
    Send the email and
    Returns true if there is no error
    '''
    emsg = EmailMessage()
    emsg.set_content(body)
    emsg["subject"] = subject
    emsg['to'] = to
    emsg["from"] = FROM_EMAIL  ##changing this doesnt really change anything

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(FROM_EMAIL, pwd)
    server.send_message(emsg)
    server.quit()
    return True

def __get_details_from_msg(msg:str):
    print(msg)
    msgs = msg.split("\n")
    print(msgs)
    to = msgs[1]
    subject = msgs[2]
    body = msgs[3:]
    return to,subject,body


def create_msg_response_for_sending_mail(msg):
    """
    This recieves the msg and sends the mails. If mail sending is sucessful, it sends a response Done
    """
    ## Get the details form message
    print("inside create")
    to, subject, body = __get_details_from_msg(msg)
    print("Printing to,su,bo: ",to,subject,body)
    # Create reply
    resp = MessagingResponse()

    ## send the email and respond accordingly
    if email_alert(subject, body, to):
        resp.message("Done 😄")
    else:
        resp.message("Not Successful 😢")
    print("Exiting mail function")
    return resp

if __name__ == '__main__':
    # email_to_send_mail = ''
    # email_alert(subject="Hey", body="Hello!", to=email_to_send_mail)
    msg = '''Send email
goyal.ayush55@gmail.com
Hello
This is a test'''
    print(__get_details_from_msg(msg))