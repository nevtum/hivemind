FROM django:latest

MAINTAINER Neville Tummon

COPY requirements/ .
RUN pip install -r requirements/common.txt

RUN mkdir -p web_app/echelon
COPY src/ /web_app/echelon

RUN mkdir -p web_app/volume
COPY volume /web_app/volume
VOLUME /web_app/volume

WORKDIR /web_app/echelon
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput
VOLUME /web_app/static
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "echelon.wsgi"]
