docker-plugin-loki
=========

Install & update the loki plugin for Docker.

Configuration in `daemon.json` is not part of this role, please see [the official documentation](https://github.com/grafana/loki/blob/master/docs/sources/clients/docker-driver/configuration.md#change-the-default-logging-driver).

Requirements
------------

  - [docker/docker-py](https://pypi.org/project/docker/)
  - dockerd, e.g. via [atosatto/dockerswarm](https://github.com/atosatto/ansible-dockerswarm/)

Role Variables
--------------

| Name           | Default Value | Description                        |
| -------------- | ------------- | -----------------------------------|
| `docker_loki_version` | `latest` | Version of the loki docker plugin |
| `docker_loki_image` | `grafana/loki-docker-driver` | The plugin Docker image to use. |
| `docker_loki_docker_unit` | `docker` | The name of the SystemD unit to restart Docker |

Dependencies
------------

n/a

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      become: true
      roles:
        - role: hostwithquantum.dockerpluginloki
          vars:
            docker_loki_version: 1.5.0

License
-------

BSD-2-Clause

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
