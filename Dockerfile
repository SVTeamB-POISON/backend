FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt


WORKDIR /app
COPY . ./

RUN adduser -D user
USER user

RUN celery -A flower worker -l info

CMD ["python","manage.py","runserver","0.0.0.0:8000"]
