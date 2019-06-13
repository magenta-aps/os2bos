# Bevillingsplatform for Ballerup (C-BUR)
[![pipeline status](https://git.magenta.dk/bevillingsplatform/bevillingsplatform/badges/develop/pipeline.svg)](https://git.magenta.dk/bevillingsplatform/bevillingsplatform/commits/develop)
[![coverage report](https://git.magenta.dk/bevillingsplatform/bevillingsplatform/badges/develop/coverage.svg)](https://git.magenta.dk/bevillingsplatform/bevillingsplatform/commits/develop)

## Installation

TL;DR: To get a running development environment run:

```bash
git@git.magenta.dk:bevillingsplatform/bevillingsplatform.git
cd bevillingsplatform
docker-compose up -d --build
```

You can now reach the frontend at http://localhost:8080. The frontend will proxy
all request to the backend.

Run backend tests with:
```
docker-compose exec bev ./manage.py test
```


### Docker

The repository contains a `Dockerfile`. This is the recommended way to install
bevillingsplatform both as a developer and in production.

All releases are pushed to Docker Hub at
[`magentaaps/bevillingsplatform`](https://hub.docker.com/r/magentaaps/bevillingsplatform)
under the `latest` tag.

To run bevillingsplatform in docker you need a running docker daemon. To install
docker we refer you to the [official
documentation](https://docs.docker.com/install/).

To configure the django inside the image, add your setting to
`/code/settings.ini`. This is easiest done by binding a file from the host
machine to this file.

The container requires a connection to a postgres database. It is configured
with the `DATABASE_*` settings.

You can start a the container with:
```bash
docker run -p 8000:8000 -v $PWD/dev-settings.ini:/code/settings.ini magentaaps/bevillingsplatform:latest
```

This will pull the image from Docker Hub and starts a container in the
foreground. The `-p 8000:8000` [binds
port](https://docs.docker.com/engine/reference/commandline/run/#publish-or-expose-port--p---expose)
`8000` of the host machine to port `8000` on the container. The `-v
$PWD/dev-settings.ini:/code/settings.ini`
[binds](https://docs.docker.com/engine/reference/commandline/run/#mount-volume--v---read-only)
the `dev-settings.ini` file into the container at the location where django will
pick it up.

If successful you should see the container migrating the database and finally
```
[2019-06-13 09:18:48 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
```

when the gunicorn server starts up. You should now be able to reach the server
from the host at ``http://localhost:8000``.


If you continue to see `01/30 Unable to connect to database.` your database
configuration most likely wrong. Remember if you set `DATABASE_HOST=localhost`
the container will try to connect to a database in the same container, not the
host machine.


#### Static files

The docker image will serve the static files for the Vue frontend, Django REST
framework and Django Admin from gunicorn both in development and in production.
Normally it is not good practice to serve static files from gunicorn for
security and performance reasons. We use
[whitenoise](https://pypi.org/project/whitenoise/) most of these conserns and
generally don't expect many users. If you still want to serve it from another
service, all the files are copied to `/static` on container startup. This can
easily be mounted to a webserver.


#### Logs

The gunicorn error log is output on `STDERR`. It can be inspected with `docker
logs`. The gunicorn access log is written to `/log/access.log`. The django log
is written to `/log/django-debug.log`.


#### User permissions

The `Dockerfile` creates and runs the application as the `bev` user.
This user will own all the files generated by the application. This user has a
``UID`` and ``GID`` of 72050.

If you want to use another ``UID/GID``, you can specify it as the
`--user=uid:gid` [overwrite
flag](https://docs.docker.com/engine/reference/run/#user) for the ``docker run``
command or [in
docker-compose](https://docs.docker.com/compose/compose-file/#domainname-hostname-ipc-mac_address-privileged-read_only-shm_size-stdin_open-tty-user-working_dir)
If you change the `UID/GID`, the `/log` and `/static` volumes may not have the
right permissions. It is recommended to only use
[bind](https://docs.docker.com/storage/bind-mounts/) if you overwrite the user
and set the same user as owner of the directory you bind.

If some process inside the container needs to write files to locations other
than `/static` or `/log`, you need to mount a volume with the right permissions.
An example is `./manage.py makemigrations` trying to write to
`/code/backend/core/migrations`. If you bind `/code` to your host system, make
sure that the user with UID 72050 have write permissions to
`backend/core/migrations`. This can be done with `chmod o+w migrations` on your
host where you grant all user permission to write.


#### Test

All the requirements for tests included in the docker image. You can run the
test from inside a container with `./manage.py test`.

##### tox
`tox` is also installed, but it tries to create a virtual environments inside
the container. This is messy an will fail because the application user does not
have permission to write files. Don't use `tox` inside the container.

### Docker-compose

You can use ``docker-compose`` to start up bevillingsplatform and related
service such as postgres and postfix.

A `docker-compose.yml` for development is included. It includes the settings
to connect them. It starts four services:

- `frontend`: the vue frontend reachable at  http://localhost:8080,
- `bev`: the django backend,
- `db`: a [postgres database server](https://hub.docker.com/_/postgres)
- `postfix`: a [postfix email server](https://hub.docker.com/r/catatnight/postfix).

Normally the backend image also serves the frontend code, but to ease frontend
development, we include a frontend service that run [`vue-cli-service
serve`](https://cli.vuejs.org/guide/cli-service.html). The frontend proxies
requests to the backend. The exact list of proxied endpoints can be seen in
`frontend/vue.config.js`.

`docker-compose.yml` also mounts the current directory in the container and
automatically restarts the server on changes to the backend files. This enables
you to edit the backend files and the server will be reloaded automatically.

To pull the images and start the three service run:
```bash
docker-compose up -d --build
```

The `-d` flag move the services to the background. You can inspect the output of
them with `docker-compose logs <name>` where `<name>` is the name of the service
in `docker-compose.yml`. The `--build` flag builds the newest docker image for
`bevillingsplatform` from the local `Dockerfile`.

To stop the service again run `docker-compose stop`. This will stop the
services, but the data will persist. To completely remove the containers and
data run `docker-compose down`.

#### Tests and shell access

To run the backend test, execute: `docker-compose exec bev ./manage.py test`. It
will connect to the running docker container and execute the tests.

To get shell access to the backend run `docker-compose exec bev bash`.

If you want to write files from inside the container, make sure the `bev` user
have permission to do so. See [User permissions](#user-permissions).

## Other Readmes

[Backend README](backend/README.md)

[Frontend README](frontend/README.md)
