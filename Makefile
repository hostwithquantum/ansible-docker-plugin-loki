SHELL=/bin/bash

IMAGE:=quay.io/ansible/molecule:3.0.4
ANSIBLE_ROLE:=ansible-docker-plugin-loki
OPTS?=--all

RUN_CMD:=docker run --rm -it \
	-v "$(CURDIR)":/tmp/$(ANSIBLE_ROLE):ro \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-w /tmp/$(ANSIBLE_ROLE) \
	--env MOLECULE_NO_LOG=no \
	$(IMAGE)

.PHONY: lint
lint:
	docker run -it --rm -v $(CURDIR):/work -w /work alpine/flake8:3.5.0 ./library

.PHONY: test
test:
	$(RUN_CMD) molecule test $(OPTS)

.PHONY: shell
shell:
	$(RUN_CMD) sh
