import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_docker_is_still_running(host):
    docker = host.service("docker")
    assert docker.is_running
    assert docker.is_enabled


def test_loki_plugin_is_installed(host):
    cmd = host.run("docker plugin ls|grep loki:latest|wc -l")
    assert cmd.rc == 0
    assert int(cmd.stdout.strip()) == 1
