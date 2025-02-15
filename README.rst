**IMPORTANT! Project is discontinued and will no longer be maintained.**


======
OS2BOS
======

|pipeline status|
|coverage report|

.. |pipeline status| image:: https://git.magenta.dk/bevillingsplatform/bevillingsplatform/badges/develop/pipeline.svg
.. |coverage report| image:: https://git.magenta.dk/bevillingsplatform/bevillingsplatform/badges/develop/coverage.svg

Installation
============

TL;DR: To get a running development environment run:

.. code-block:: bash

   git clone git@git.magenta.dk:bevillingsplatform/bevillingsplatform.git
   cd bevillingsplatform
   docker-compose up -d


You can now reach the frontend at http://localhost:8080. The frontend will proxy
all request to the backend.

Run backend tests with:

.. code-block:: bash

   docker-compose exec bev pytest



Docker
------

The repository contains a ``Dockerfile``. This is the recommended way to install
bevillingsplatform both as a developer and in production.

All releases are pushed to Docker Hub at `magentaaps/bevillingsplatform
<https://hub.docker.com/r/magentaaps/bevillingsplatform>`_
under the ``latest`` tag.

To run bevillingsplatform in docker you need a running docker daemon. To install
docker we refer you to the `official documentation
<https://docs.docker.com/install/>`_.

To configure the django inside the image, add your setting to
``/code/settings.ini``. This is easiest done by binding a file from the host
machine to this file.

The container requires a connection to a postgres database server. It is
configured with the ``DATABASE_*`` settings. The database server must have a user
and a database object. It can be created with the help of
``/docker/postgres-initdb.d/20-create-db-and-user.sh``. This file can easily be
mounted into ``/docker-entrypoint-initdb.d/`` in `the official postgres docker image
<https://hub.docker.com/_/postgres>`_.

You can start the container with:

.. code-block:: bash

   docker run -p 8000:8000 -v $PWD/dev-settings.ini:/code/settings.ini magentaaps/bevillingsplatform:latest


This will pull the image from Docker Hub and starts a container in the
foreground. The ``-p 8000:8000`` `binds port
<https://docs.docker.com/engine/reference/commandline/run/#publish-or-expose-port--p---expose>`_
``8000`` of the host machine to port ``8000`` on the container. The ``-v
$PWD/dev-settings.ini:/code/settings.ini``
`binds
<https://docs.docker.com/engine/reference/commandline/run/#mount-volume--v---read-only>`_
the ``dev-settings.ini`` file into the container at the location where django will
pick it up.

If successful you should see the container migrating the database and finally

.. code-block::

   [2019-06-13 09:18:48 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)


when the gunicorn server starts up. You should now be able to reach the server
from the host at ``http://localhost:8000``.


If you continue to see ``01/30 Unable to connect to database.`` your database
configuration most likely wrong. Remember if you set ``DATABASE_HOST=localhost``
the container will try to connect to a database in the same container, not the
host machine.


Static files
^^^^^^^^^^^^

The docker image will serve the static files for the Vue frontend, Django REST
framework and Django Admin from gunicorn both in development and in production.
Normally it is not good practice to serve static files from gunicorn for
security and performance reasons. We use `whitenoise
<https://pypi.org/project/whitenoise/>`_ to address most of these concerns and
generally don't expect many users. If you still want to serve it from another
service, all the files are copied to ``/static`` on container startup. This can
easily be mounted to a webserver.


Logs
^^^^

For logging we use the builtin ``logging`` module used by `Django`_.
Logs are written to the ``/log/`` directory inside the container.

The ``/log/`` folder is mapped to the host systems ``log/`` folder in local development and ``/var/log/os2bos/`` anywhere else.

We log the following:

* Error log - the gunicorn error log is output on ``STDERR`` as well as in ``/log/error.log``. It can be inspected with ``docker logs``.

* Access log - The gunicorn access log is output on ``STDOUT`` as well as in ``/log/access.log``. It can be inspected with ``docker logs``.

* Django debug log - The django log is written to ``/log/django-debug.log``.

* Audit log - We log all non-idempotent requests (``POST``/``PUT``/``PATCH``/``DELETE``) in the audit log specifying the request endpoint and user making the request. The log is written to ``/log/audit.log``.

* Export to Prism log - Log related to the PRISM exports management command. The log is written to ``/log/export_to_prism.log``.

* Mark Payments Paid log - Log related to the marking payments paid management command. The log is written to ``mark_payments_paid.log``.

* Generate Payments Report log - Log related to generating the payment reports. The log is written to ``/log/generate_payments_report.log``.

* Cron mail logs - Logs related to the `Django mailer app`_. The logs are written to ``cron_mail.log``, ``cron_mail_deferred.log``, ``cron_mail_purge.log``.

.. _Django: https://docs.djangoproject.com/en/dev/topics/logging/
.. _Django mailer app: https://github.com/pinax/django-mailer/

User permissions
^^^^^^^^^^^^^^^^

The `Dockerfile` creates and runs the application as the `bev` user.
This user will own all the files generated by the application. This user has a
``UID`` and ``GID`` of 72050.

If you want to use another ``UID/GID``, you can specify it as the
``--user=uid:gid`` `overwrite flag
<https://docs.docker.com/engine/reference/run/#user>`_. for the ``docker run``
command or `in docker-compose
<https://docs.docker.com/compose/compose-file/#domainname-hostname-ipc-mac_address-privileged-read_only-shm_size-stdin_open-tty-user-working_dir>`_.
If you change the ``UID/GID``, the ``/log`` and ``/static`` volumes may not have the
right permissions. It is recommended to only use
`bind
<https://docs.docker.com/storage/bind-mounts/>`_ if you overwrite the user
and set the same user as owner of the directory you bind.

If some process inside the container needs to write files to locations other
than ``/static`` or ``/log``, you need to mount a volume with the right permissions.
An example is ``./manage.py makemigrations`` trying to write to
``/code/backend/core/migrations``. If you bind ``/code`` to your host system, make
sure that the user with UID 72050 have write permissions to
``backend/core/migrations``. This can be done with ``chmod o+w migrations`` on your
host where you grant all user permission to write.


Test
^^^^

All the requirements for tests included in the docker image. You can run the
test from inside a container with ``pytest``.

tox
"""

``tox`` is also installed, but it tries to create a virtual environments inside
the container. This is messy and will fail because the application user does not
have permission to write files. Don't use ``tox`` inside the container.


Docker-compose
--------------

You can use ``docker-compose`` to start up bevillingsplatform and related
services such as postgres and postfix.

A ``docker-compose.yml`` for development is included. It includes the settings
to connect them. It starts the following services:

- `frontend`: the vue frontend reachable at  http://localhost:8080
- `bev`: the django backend
- `db`: a OS2BOS specific `postgres database server`_
- `bev-cron`: `supercronic`_, a job runner running our cronjobs
- `idp`: a local version of the IdP running our version of `SimpleSAMLphp`_
- `postfix`: a `postfix email server`_

.. _postfix email server: https://hub.docker.com/r/catatnight/postfix
.. _postgres database server: https://git.magenta.dk/bevillingsplatform/postgres-os2bos
.. _supercronic: https://github.com/aptible/supercronic
.. _SimpleSAMLphp: https://simplesamlphp.org/

Normally the backend image also serves the frontend code, but to ease frontend
development, we include a frontend service that run `vue-cli-service serve
<https://cli.vuejs.org/guide/cli-service.html>`_. The frontend proxies
requests to the backend. The exact list of proxied endpoints can be seen in
``frontend/vue.config.js``.

``docker-compose.yml`` also mounts the current directory in the container and
automatically restarts the server on changes to the backend files. This enables
you to edit the backend files and the server will be reloaded automatically.

To pull the images and start the services run:

.. code-block:: bash

   docker-compose up -d --build


The ``-d`` flag move the services to the background. You can inspect the output of
them with ``docker-compose logs <name>`` where ``<name>`` is the name of the service
in ``docker-compose.yml``. The ``--build`` flag builds the newest docker image for
`bevillingsplatform` from the local ``Dockerfile``.

To stop the service again run `docker-compose stop`. This will stop the
services, but the data will persist. To completely remove the containers and
data run ``docker-compose down -v``.


Tests and shell access
======================

To run the backend test, execute: ``docker-compose exec bev ./manage.py test``. It
will connect to the running docker container and execute the tests.

To get shell access to the backend run ``docker-compose exec bev bash``.

If you want to write files from inside the container, make sure the `bev` user
have permission to do so. See `User permissions`_.

Tests can also be executed locally with tox:

.. code-block:: bash

   tox -e test

Code coverage
=============
We adhere to a code coverage of 100%.

After running the test-suite a coverage report can be generated locally with tox:

.. code-block:: bash

   tox -e coverage


Documentation
=============

The documentation exists at `Read the Docs`_ and can be generated locally with tox:

.. code-block:: bash

   tox -e docs

When changes are introduced to the Django models, update and commit the database model graph for use in documentation:

.. code-block:: bash

   tox -e graph

.. _Read the Docs: https://os2bos.readthedocs.io/en/latest/

Code standards
==============
The Python code is enforced with the following standards:

- `black`_
- `flake8`_
- `pydocstyle`_ (`PEP257`_)

.. _black: https://github.com/psf/black
.. _flake8: https://gitlab.com/pycqa/flake8
.. _PEP257: https://www.python.org/dev/peps/pep-0257/
.. _pydocstyle: http://www.pydocstyle.org/en/latest/

Adherence to these standards can be checked locally with tox:

.. code-block:: bash

   tox -e lint



Licensing
=========

Copyright (c) 2019 Magenta Aps

Bevillingsplatform is free software; you may use, study, modify and
distribute it under the terms of version 2.0 of the Mozilla Public
License. See the LICENSE file for details. If a copy of the MPL was not
distributed with this file, You can obtain one at
http://mozilla.org/MPL/2.0/.

All source code in this and the underlying directories is subject to
the terms of the Mozilla Public License, v. 2.0.

The core version of the code is located here: https://github.com/OS2bos/os2bos/.
