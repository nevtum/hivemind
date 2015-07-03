#!/bin/bash

docker run -it -d --name pgdb \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_USER=echelon_user \
  postgres
