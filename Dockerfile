FROM python:3.6.1

MAINTAINER Neville Tummon

RUN apt-get update && apt-get install -y \
    wget curl nano postgresql-client

ADD requirements/ .
RUN pip install -r prod.txt

RUN mkdir -p web_app/hivemind
ADD src/ entry-point.sh /web_app/hivemind/

WORKDIR /web_app/hivemind

CMD ["sh", "entry-point.sh"]
