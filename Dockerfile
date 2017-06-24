FROM django:1.8.7

MAINTAINER Neville Tummon

RUN apt-get update && apt-get install -y \
    wget curl nano

ADD requirements/ .
RUN pip install -r prod.txt

RUN mkdir -p web_app/echelon
ADD src/ entry-point.sh /web_app/echelon/

WORKDIR /web_app/echelon

CMD ["sh", "entry-point.sh"]
