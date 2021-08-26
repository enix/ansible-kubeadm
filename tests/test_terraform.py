import ansible_runner
import logging
import os
import pytest
import tftest


@pytest.fixture
def spawn():
    tf = tftest.TerraformTest(os.path.join(os.path.dirname(__file__), 'terraform'))
    tf.setup(cleanup_on_exit=False)
    tf.apply()
    yield tf.output()
    if os.environ.get('TERRAFORM_KEEP', 'false').lower() not in ['true', '1']:
        tf.destroy()


@pytest.fixture
def inventory(spawn):
    return '{}/terraform/{}'.format(os.path.dirname(__file__), spawn['inventory'])


@pytest.fixture
def running_vm(inventory):
    result = ansible_runner.run(
        inventory=inventory,
        host_pattern='all',
        module='wait_for_connection'
    )
    fix_dns = ansible_runner.run(
        envvars={'ANSIBLE_HOST_KEY_CHECKING': 'false'},
        inventory=inventory,
        playbook=os.path.join(os.path.dirname(__file__), 'playbooks/fix-dns.yml')
    )
    assert fix_dns.status == 'successful'


@pytest.fixture
def prepared_vm(inventory, running_vm):
    docker = ansible_runner.run(
        envvars={'ANSIBLE_HOST_KEY_CHECKING': 'false'},
        inventory=inventory,
        playbook=os.path.join(os.path.dirname(__file__), 'playbooks/docker.yml')
    )
    assert docker.status == 'successful'


def ansible_retry(count, func):
    def wrapper(*args, **kwargs):
        for counter in range(count, -1, -1):
            try:
                ansible_result = func(*args, **kwargs)
                if ansible_result.status == 'successful':
                    return ansible_result
                continue
            except Exception as exc:
                logging.exception(str(exc))
                if counter == 0:
                    raise
        return ansible_result
    return wrapper


def install(inventory, **kwargs):
    for playbook in ['00-apiserver-proxy.yml',
                     '01-site.yml']:
        result = ansible_runner.run(
            envvars={'ANSIBLE_HOST_KEY_CHECKING': 'false',
                     'ANSIBLE_FORCE_COLOR': 'true'},
            inventory=inventory,
            playbook=os.path.join(os.path.dirname(__file__), '../playbooks/', playbook),
            **kwargs
        )
    return result


def kube_router(inventory, **kwargs):
    return ansible_runner.run(
        envvars={'ANSIBLE_HOST_KEY_CHECKING': 'false',
                 'ANSIBLE_FORCE_COLOR': 'true'},
        inventory=inventory,
        module='command',
        module_args='kubectl apply -f https://raw.githubusercontent.com/cloudnativelabs/kube-router/master/daemonset/kubeadm-kuberouter.yaml',
        host_pattern='{{ kube_cp_group|default("kube_control_plane") }}[0]',
        **kwargs
    )


def test_install(inventory, prepared_vm):
    result = ansible_retry(2, install)(inventory, cmdline=os.environ.get('ANSIBLE_EXTRA_ARGS', None))
    assert result.status == 'successful'
    result = ansible_retry(1, kube_router)(inventory, cmdline=os.environ.get('ANSIBLE_EXTRA_ARGS', None))
    assert result.status == 'successful'


def test_upgrade(inventory, prepared_vm):
    result = install(inventory)
    assert result.status == 'successful'
    result = kube_router(inventory)
    assert result.status == 'successful'
    result = install(inventory, extravars={'kube_version': '1.18'})
    assert result.status == 'successful'
