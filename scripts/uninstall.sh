#!/bin/bash

docker stop echelon-container
docker rm echelon-container
docker stop pgdb
docker rm pgdb
