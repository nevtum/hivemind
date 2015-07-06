Development
==================

Before starting development make sure a fresh isolated python virtual environment is installed and activated:

    $ virtualenv <environment name>
    $ source <environment name>/bin/activate

If you are developing on Windows run the following from the command line:

		$ <environment name>\Scripts\activate

Install the required PyPi packages listed within the dev.txt:

    $ pip install -r <path to file>/dev.txt

To get started with a debug instance of the django server run the following:

    $ python manage.py runserver

Install new database instance (Production only)
==================

Echelon writes and reads from a PostgreSQL database within a separate Docker container instance. To create this new container go into the scripts folder and execute the following:

    $ sh install_pgsql.sh

Build
==================

When deploying a production ready instance of BMM Echelon using Docker make sure Docker is properly installed on the system prior to building an image. To build a Docker image  of the project go to the directory where this README file is located and type the following:

    $ docker build -t <image name> .

Deploy
==================

To run a new container from the built image type the following:

    $ docker run -it -d --name <app name> -p <host port>:8015 --link <db name>:localhost <image name>

Alternatively, run the following in the scripts folder:

    $ sh release_app.sh

This script will conveniently build and (re)deploy a new instance of Echelon. Use this script when updating to a new version of the app.

Populating database for 1st time (Production only)
==================

The fresh db install will initially have no data so there are a few more steps needed to get everything running properly in production.

* Create database tables from Django models
* Create an admin user (superuser)

This only needs to be done once and not everytime a new Echelon release is scheduled. Make sure an Echelon container is running and linked to the database container:

    $ docker exec -it <app name> /bin/bash

Inside the container, run these commands, then exit out of the container:

    $ python manage.py migrate (manage.py must point to prod)
    $ python manage.py createsuperuser (manage.py must point to prod)
