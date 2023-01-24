FROM python:3.10

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip setuptools wheel

RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx

RUN pip install -r /requirements.txt

WORKDIR /app
COPY . ./

CMD ["python","manage.py","runserver","0.0.0.0:8000"]