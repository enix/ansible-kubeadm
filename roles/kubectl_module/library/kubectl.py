#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from ansible.module_utils.basic import AnsibleModule


class Kubectl(object):

    def __init__(self, namespace, resource_type, resource_definition, state,
                 name, extra_args=None, kubeconfig=None, verify_ssl=True):
        self.namespace = namespace
        self.resource_type = resource_type
        self.name = name
        self.resource_definition = resource_definition
        self.state = state
        self.kubeconfig = kubeconfig
        self.extra_args = extra_args
        self.verify_ssl = verify_ssl
        self._kubectl = None

    @property
    def kubectl(self):
        if not self._kubectl:
            raise KubectlError('No kubectl binary has been found !')
        return self._kubectl

    @kubectl.setter
    def kubectl(self, binary):
        self._kubectl = binary

    def execute(self):
        if self.state in ['get', 'facts']:
            return self.get()

    def get(self):
        if not self.resource_type:
            self.module.fail_json(msg='resource_type is required to query cluster')
        cmd = ['get', self.resource_type, '-o', 'json']
        if self.name:
            cmd.append(self.name)
        out = self._run_kubectl(cmd)
        if self.name:
            return {'item': json.loads(out)}
        else:
            return {'items': json.loads(out)['items']}

    def _run_kubectl(self, cmd, stdin=None):
        args = [self.kubectl]
        if self.kubeconfig:
            args.append('--kubeconfig=' + self.kubeconfig)
        if not self.verify_ssl:
            args.append('--insecure-skip-tls-verify=true')
        if self.namespace:
            args.append('--namespace=' + self.namespace)
        args.extend(cmd)
        if self.extra_args:
            args.extend(self.extra_args)
        try:
            rc, out, err = self.run_command(args, data=stdin)
            if rc != 0:
                self.fail_json(
                    msg='error running kubectl (%s) command (rc=%d), out= '
                        '\'%s\', err=\'%s\'' % (' '.join(args), rc, out, err))
        except Exception as exc:
            self.fail_json(
                msg='error running kubectl (%s) command: %s' % (' '.join(args), str(exc)))
        return out


class KubectlError(Exception):
    """Error from Kubectl Module"""


class KubectlAnsible(Kubectl, AnsibleModule):

    def __init__(self):
        AnsibleModule.__init__(
            self,
            argument_spec=dict(
                namespace=dict(type='str'),
                resource_type=dict(type='str'),
                name=dict(type='str'),
                resource_definition=dict(type='list'),
                state=dict(default='present', choice=['present', 'facts', 'get', 'absent']),
                binary=dict(type='str'),
                kubeconfig=dict(type='str'),
                extra_args=dict(type='list'),
                verify_ssl=dict(type='bool', default=True)
            ),
            supports_check_mode=True,
        )
        binary = self.params.pop('binary')
        Kubectl.__init__(self, **self.params)
        if binary is None:
            self.kubectl = self.get_bin_path('kubectl', True)
        else:
            self.kubectl = binary


def main():
    module = KubectlAnsible()
    try:
        res_dict = module.execute()
    except KubectlError as exc:
        module.fail_json(msg=exc.args[0])
    else:
        module.exit_json(**res_dict)


if __name__ == '__main__':
    main()
