FROM django:latest

MAINTAINER "Neville Tummon"

RUN mkdir -p echelon
COPY . /echelon
WORKDIR /echelon
RUN mkdir -p volume
VOLUME /echelon/volume

RUN pip install -r requirements.txt
RUN python manage.py syncdb --noinput
RUN python manage.py migrate --noinput
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "echelon.wsgi"]
