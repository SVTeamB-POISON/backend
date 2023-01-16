FROM python:3.10

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt


RUN pip install -r /requirements.txt

WORKDIR /app
COPY . ./



#CMD ["python","manage.py","runserver"]