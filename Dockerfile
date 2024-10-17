FROM python:3.10-slim-buster

WORKDIR /flaskapp

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY . .

EXPOSE 5000

CMD [ "gunicorn", "app:app"]
