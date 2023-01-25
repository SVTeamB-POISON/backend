FROM python:3.10

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt


RUN pip install -r /requirements.txt

WORKDIR /app
COPY . ./

<<<<<<< HEAD
# CMD ["python","manage.py","runserver","0.0.0.0:8000"]
=======
#CMD ["python","manage.py","runserver"]
>>>>>>> parent of 48d2d26... Merge pull request #103 from SVTeamB-POISON/refactor/#102
