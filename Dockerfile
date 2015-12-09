FROM django:latest

MAINTAINER Neville Tummon

ADD requirements/ .
RUN pip install -r dev.txt

RUN mkdir -p web_app/echelon
ADD src/ entry-point.sh /web_app/echelon/

WORKDIR /web_app/echelon

CMD ["sh", "entry-point.sh"]
