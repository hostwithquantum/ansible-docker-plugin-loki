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


def test_loki_plugin_version(host):
    ref = "docker.io/grafana/loki-docker-driver"
    item = ".PluginReference"

    cmd = []
    cmd.append("curl -s --unix-socket /var/run/docker.sock")
    cmd.append("http:/plugins")
    cmd.append("|")
    cmd.append("jq -r")
    cmd.append("'.[]|select(%s|startswith(\"%s:\"))|%s'" % (item, ref, item))

    output = host.run(" ".join(cmd))

    assert output.rc == 0
    assert '1.5.0' in output.stdout


def test_logging_container(host):
    output = host.run("docker service inspect --pretty random-logger")
    print(output.stdout)

    ps = host.run("docker ps -a")
    print(ps.stdout)

    containers = host.docker.get_containers(status="running")
    assert len(containers) == 1
