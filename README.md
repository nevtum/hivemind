Build
======

To build a docker image go to directory where this README file is located and type the following:

    $ docker build -t <image name>

Deploy
======

To run instance of docker image type the following:

    $ docker run -it -d -p <host port>:8000 <image name>
