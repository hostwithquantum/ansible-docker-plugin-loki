#!/usr/bin/python

# Copyright: (c) 2021, Planetary Quantum GmbH <oss@planetary-quantum.com>
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# ansible dependencies
from ansible.module_utils.basic import AnsibleModule

# code dependencies
import docker
from docker.models.plugins import Plugin
from docker.errors import NotFound, APIError, DockerException


# This is a work-around because I was trying to smart and use the Docker API.
def _disable(the_plugin, client):
    # type: (Plugin, docker.client.DockerClient) -> Plugin
    if not the_plugin.enabled:
        return True

    result = client.api.post(('/plugins/%s/disable?force=1' % the_plugin.name))
    result.raise_for_status()
    result.close()

    the_plugin.reload()

    return the_plugin


def _extract_version(attrs):
    # type: (dict) -> str
    return attrs['PluginReference'].split(':')[1]


def _handle_exception(the_message, the_exception, module, result):
    # type: (str, Exception, AnsibleModule, dict) -> None

    error_msg = 'unknown'
    if hasattr(the_exception, 'message'):
        error_msg = the_exception.message

    module.fail_json(
        msg=(the_message % error_msg),
        **result)


def _install(version, client, result):
    # type: (str, docker.client.DockerClient, dict) -> dict

    try:
        plugin = client.plugins.get(result['name'])  # type: Plugin
        return result
    except NotFound:
        plugin = client.plugins.install(version, result['name'])  # type: Plugin
        if not plugin.enabled:
            plugin.enable()

        result['new_version'] = _extract_version(plugin.attrs)
        result['changed'] = True
        return result


def _upgrade(plugin_version, client, result):
    # type: (str, docker.client.DockerClient, dict) -> dict

    try:
        plugin = client.plugins.get(result['name'])  # type: Plugin
    except NotFound:
        raise Exception(
            msg=('The plugin "%s" is not installed' % result['name']))

    result['old_version'] = _extract_version(plugin.attrs)

    if plugin.enabled:
        plugin = _disable(plugin, client)

    # version contains: namespace/image:version
    logs = plugin.upgrade(plugin_version)
    for log_line in logs:
        result['debug'].append({'log': log_line})

    if not plugin.enabled:
        plugin.enable()

    result['debug'].append({"attrs": plugin.attrs})

    result['new_version'] = _extract_version(plugin.attrs)

    if result['new_version'] != result['old_version']:
        result['changed'] = True

    return result


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        version=dict(type='str', required=True),
        state=dict(
            type='str',
            default='install',
            choices=['install', 'upgrade'])
    )

    result = dict(
        changed=False,
        name='',
        new_version='',
        old_version='',
        debug=[]
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    result['name'] = module.params['name']

    try:
        client = docker.from_env()  # type: docker.client.DockerClient
    except DockerException as e:
        _handle_exception(
            'Unable to create a docker-client: %s',
            e,
            module,
            result)

    try:
        if module.params['state'] == 'upgrade':
            result = _upgrade(
                module.params['version'],
                client,
                result)
        else:
            result = _install(
                module.params['version'],
                client,
                result)

        module.exit_json(**result)
    except APIError as e:
        _handle_exception(
            'A Docker API error occurred: %s',
            e,
            module,
            result)
    except Exception as e:
        _handle_exception(
            'An exception occurred: %s',
            e,
            module,
            result)


def main():
    run_module()


if __name__ == '__main__':
    main()
