#!/bin/bash

docker build -t echelon-img ../.

# BEWARE: this command removes previous instances of container
docker stop echelon-container
docker rm echelon-container

docker run -it -d --name echelon-container \
  -p 8000:8000 \
  --link pgdb:localhost \
  echelon-img
