Development
======

Before starting development make sure a fresh isolated python virtual environment is installed and activated:

    $ virtualenv <environment name>
    $ source <environment name>/bin/activate

If you are developing on Windows run the following from the command line:

		$ <environment name>\Scripts\activate

Install the required PyPi packages listed within the dev.txt:

    $ pip install -r <path to file>/dev.txt

To get started with a debug instance of the django server run the following:

    $ python manage.py runserver

Build
======

When deploying a production ready instance of BMM Echelon using Docker make sure Docker is properly installed on the system prior to building an image. To build a Docker image  of the project go to the directory where this README file is located and type the following:

    $ docker build -t <image name> .

Deploy
======

To run a new container from the built image type the following:

    $ docker run -it -d --name <container name> -p <host port>:80 <image name>

Once running there are volumes that are exposed from the container which can be accessed using other Docker containers. It is recommended to spin up a Busybox container to transfer files in and out of the Echelon container. Make sure Echelon container is currently running:

    $ docker run -it --rm --volumes-from <container name> busybox /bin/sh
