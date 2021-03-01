#!/usr/bin/python

# Copyright: (c) 2021, Planetary Quantum GmbH <oss@planetary-quantum.com>
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# ansible dependencies
from ansible.module_utils.basic import AnsibleModule

# code dependencies
import docker


def run_module():
    module_args = dict(
        name=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        name='',
        disabled=False,
        installed=False,
        ref='',
        version='',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    result['name'] = module.params['name']

    client = docker.from_env()

    try:
        plugin = client.plugins.get(module.params['name'])
        result['installed'] = True
        result['disabled'] = not plugin.enabled
        result['ref'] = plugin.attrs['PluginReference']
        result['version'] = result['ref'].split(':')[1]

    except docker.errors.DockerException:
        result['installed'] = False

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
