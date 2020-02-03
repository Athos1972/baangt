FROM python:3.7.5

LABEL Testrun application

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "application.py"
ENV FLASK_DEBUG True

RUN mkdir /testrun
WORKDIR /testrun

COPY requirements.txt requirements.txt

RUN python -m venv venv

RUN pip install pipenv && \
    pipenv install --dev

ADD . /testrun

EXPOSE 5000

RUN pipenv run python populate_db.py
CMD pipenv run flask run --host=0.0.0.0