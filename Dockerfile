FROM ubuntu:latest

MAINTAINER "Neville Tummon"

RUN apt-get update && apt-get install -y python3-pip

RUN mkdir -p echelon
COPY . /echelon
WORKDIR /echelon

RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "echelon.wsgi"]
