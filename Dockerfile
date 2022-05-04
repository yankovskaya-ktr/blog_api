FROM python:3.9.12
WORKDIR /code
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY /blog_api .
CMD gunicorn blog_api.wsgi:application --bind 0.0.0.0:8000
