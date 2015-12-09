FROM django:latest

MAINTAINER Neville Tummon

RUN apt-get update && apt-get install nginx -y
RUN rm /etc/nginx/sites-enabled/default
ADD nginx/ /etc/nginx/sites-enabled

ADD requirements/ .
RUN pip install -r dev.txt

RUN mkdir -p web_app/echelon
ADD src/ entry-point.sh /web_app/echelon/

WORKDIR /web_app/echelon

CMD ["sh", "entry-point.sh"]
