#!/usr/bin/python

# Copyright: (c) 2021, Planetary Quantum GmbH <oss@planetary-quantum.com>
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# ansible dependencies
from ansible.module_utils.basic import AnsibleModule

# code dependencies
import docker


def _extract_version(attrs):
    return attrs['PluginReference'].split(':')[1]


def _install(name, version, client, result):
    try:
        plugin = client.plugins.get(name)
        return result
    except docker.errors.NotFound:
        plugin = client.plugins.install(version, name)
        if not plugin.enabled:
            plugin.enable()

        result['new_version'] = _extract_version(plugin.attrs)
        result['changed'] = True
        return result


def _upgrade(name, version, client, result):
    result['name'] = name

    try:
        plugin = client.plugins.get(name)
    except docker.errors.NotFound:
        raise Exception(msg=('The plugin "%s" is not installed' % name))

    result['old_version'] = _extract_version(plugin.attrs)

    if plugin.enabled:
        plugin.disable()

    # version contains: namespace/image:version
    logs = plugin.upgrade(version)
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
        client = docker.from_env()
    except docker.errors.DockerException:
        module.fail_json(msg='Unable to create a docker-client', **result)

    if module.params['state'] == "upgrade":
        result = _upgrade(
            module.params['name'],
            module.params['version'],
            client,
            result)
    else:
        result = _install(
            module.params['name'],
            module.params['version'],
            client,
            result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
