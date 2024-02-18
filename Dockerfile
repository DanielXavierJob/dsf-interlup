FROM python:3.12.0-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip install uwsgi
COPY . .
CMD [ "uwsgi","--socket", "0.0.0.0:5000", "--protocol=http", "-w", "wsgi:application" ]