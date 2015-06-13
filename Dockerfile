FROM django:latest

MAINTAINER Neville Tummon

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p echelon
COPY src/ /echelon

RUN mkdir -p volume
COPY volume /volume
VOLUME /volume

WORKDIR /echelon
RUN python manage.py syncdb --noinput
RUN python manage.py migrate --noinput
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "echelon.wsgi"]
