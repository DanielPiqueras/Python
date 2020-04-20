Readme
======

This meta repository contains sub-modules necessary to run Ebiblio :

* ebiblio-api for the back-end
* ebiblio-front for the front-end

It also contains the necessary files to run a Ebiblio instance in docker containers.

**You don't need to use the submodules** to run you Ebiblio instance, you can use your local repositories.

Quick start guide
-----------------

* Install docker and docker-compose

Next steps are with the jason.gass/ebiblio repository (this one) :

* Clone the repository.

```
git clone git@desarrollo.vozelia.com:jason.gass/ebiblio.git
```

* Initialize the meta repository.

```
cd ebiblio
git submodule init
git submodule update
# Get on the master branch for all modules
git submodule foreach git checkout master
git submodule foreach git pull
```


* Copy and edit the environment file with the locations of files on your computer
* Run the following commands in the folder for the configuration you have chosen :

```
docker-compose up
```

For more detailed informations, see below.

Init the meta repo
------------------

This repo uses Git Submodules to manage different repositories. You need to init them after having cloned the repository:

```
git submodule init
git submodule update
```

> Official documentation : https://git-scm.com/book/en/v2/Git-Tools-Submodules

Run Ebiblio locally
------------------

The main goal of this configuration is to be able to run a local version of Ebiblio without having to install all prerequisites and configuration on the host machine.

### Install Docker and Docker Compose

From the installation documentation, see the [Docker](https://docs.docker.com/engine/installation).

### Update the environment file

First, you have to copy the `.env.sample` files under the `docker/local` or the `docker/dev` directory and name them `.env`. You can then update them with the actual values of the paths you want to use. Those are independant, even though they contain the same keys. Updates to the metarepo, the docker files and env configuration will be the subject of announces to tell when to merge master.

The environment file contains absolute paths to :

* the **ALLOWED_HOSTS** variable, add your IP at the end of the line
* the **FRONT_URL** variable, add your IP and the docker container port for the FRONT => `http://localhost:3000`
* the **REACT_APP_API_URL** variable, add your IP and the docker container port for the API => `http://localhost:8000`
* the **ebiblio-api** directory, the generic default is `<path/to/django/project>`
* the **ebiblio-front** directory, the generic default is `<path/to/front/project>`

**NOTE:** The Ebiblio directory can be the meta repository, but if you don't want to use it, you have to mount a directory that contains all the repositories that are needed, as referenced in the introduction.

### Run Ebiblio in local configuration

When working in command line, get in the `docker/local` directory, and run the command `docker-compose up`.

* If you get an error message concerning mounting a directory on a file, or vice-versa, check your environment file for an incorrect path.

Use the containers
------------------

### Use only one docker not the both
> Requirements: **Run one time the docker-compose file to have the docker images**

If you don't need to use both dockers you can do that executing the following command:

```
docker-compose ps

          Name                         Command                State     Ports
-----------------------------------------------------------------------------
local_ebiblio_api_1         sh -c python manage.py mak ...
local_ebiblio_front_1       npm start
local_ebiblio_storybook_1   npm run storybook 
```

1. To start: `docker start <container_name>`
2. To stop: `docker stop <container_name>`
3. To see logs: `docker logs -f <container_name>`

### Get inside the container

To get inside one of these containers, you can use the following command :

`docker exec -it <container_name> /bin/bash`

This command launches bash inside the container and keeps it opened for you to interact with it. `sh` and `zsh` are also available.

Troubleshooting
---------------

> A container is throwing an error about a process already running, what can I do ?

Have you tried turning it off and on again? You can do that using :

```
docker-compose down
docker-compose up
```

> The service won't start because of "No such file or directory" !

Check your `.env` file for the corresponding configuration. You might have forgotten to update the paths leading to your repository and/or configuration files.
