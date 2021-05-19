SHELL=/bin/bash

IMAGE:=quay.io/ansible/molecule:3.1.4
ANSIBLE_ROLE:=ansible-docker-plugin-loki
MOLECULE_NO_LOG?=no
OPTS?=--all

RUN_CMD:=docker run --rm -it \
	-v "$(CURDIR)":/tmp/$(ANSIBLE_ROLE) \
	-w /tmp/$(ANSIBLE_ROLE)

.PHONY: flake8
flake8:
	$(RUN_CMD) alpine/flake8:3.5.0 ./library

.PHONY: test
test:
	$(RUN_CMD) \
	-v /var/run/docker.sock:/var/run/docker.sock \
	--env MOLECULE_NO_LOG=$(MOLECULE_NO_LOG) \
	$(IMAGE) molecule --debug test $(OPTS)

.PHONY: shell
shell:
	$(RUN_CMD) $(IMAGE) sh
