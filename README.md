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

    $ python dev_manage.py runserver

Build & Deploy
==================

When deploying a production ready instance of BMM Echelon using Docker make sure Docker and Docker Compose is properly installed on the system prior to building an image. To build a Docker image  of the project go to the directory where this README file is located and type the following:

    $ docker-compose build
    $ docker-compose up -d

The same sequence of commands can be used when updating a new version of the BMM Echelon django application. But BE CAREFUL not to change any Docker settings for the PostGreSQL database container unless you're looking to delete ALL DATA in the existing database instance container.

Populating database for 1st time (Production only)
==================

The fresh db install will initially have no data so there are a few more steps needed to get everything running properly in production.

* Create database tables from Django models
* Create an admin user (superuser)

This only needs to be done once and not everytime a new Echelon version is released. Make sure an Echelon container is running and linked to the database container:

    $ docker exec -it <web app name> bash

Inside the container, run these commands, then exit out of the container:

    $ python manage.py migrate
    $ python manage.py createsuperuser
