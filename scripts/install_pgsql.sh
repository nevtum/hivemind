#!/bin/bash

docker run -it -d --name pgdb \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_USER=echelon_user \
  postgres
  # -p 5432:5432 \
