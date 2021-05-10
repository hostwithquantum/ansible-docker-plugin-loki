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

Use the role like so:

    - hosts: servers
      roles:
        - role: hostwithquantum.dockerpluginloki
          vars:
            docker_loki_version: 1.5.0


On `become: true`: The role assumes a reasonable Docker setup where `root` is only required to restart `dockerd`. Ansible will need to be able to _sudo up_ to perform the restart after installation or upgrade. All other interactions (e.g. `docker plugin install`) should work as non-root user. If you use Docker as `root`, you may have to add `become: true` in your playbook.

License
-------

BSD-2-Clause

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
