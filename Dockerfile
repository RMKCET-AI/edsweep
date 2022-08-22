FROM python:latest

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update

# RUN apt-get upgrade

RUN pip install --upgrade pip setuptools --user --no-cache-dir

RUN pip install -r requirements.txt

RUN apt-get install -y nodejs

RUN apt-get install -y npm

COPY . /app

EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]

