import itertools
import os
import re

import ansible_runner


def install_ansible(virtualenv, version=None):
    virtualenv.debug = True
    requirements_txt = os.path.join(os.path.dirname(__file__), "../requirements.txt")
    virtualenv.run(["pip", "install", "-r", requirements_txt])
    if version is None:
        virtualenv.install_package("ansible")
    else:
        virtualenv.install_package("ansible", version=version)


def install_galaxy_deps(virtualenv):
    test_dir = os.path.join(os.path.dirname(__file__), "..")
    virtualenv.run(
        [
            "ansible-galaxy",
            "install",
            "-r",
            os.path.join(test_dir, "ansible.requirements.yml"),
            "-p",
            os.path.join(test_dir, "playbooks/roles"),
        ]
    )


def run_ansible_playbook(
    virtualenv, playbooks, dry_run=False, ansible_extra_args=None, **kwargs
):
    if isinstance(playbooks, str):
        playbooks = [playbooks]
    playbooks = [
        os.path.join(os.path.dirname(__file__), "../..", pbk) for pbk in playbooks
    ]
    # ansible_runner has several "bugs":
    # - Don't accept multiple playbooks on the parameter "playbook" (which is supposed to accept list)
    # - If you pass custom binary it cannot say if ansible or ansible-playbook so doesn't inject playbook anymore
    # => thus, pass playbooks as cmdline
    envvars = dict(os.environ)
    envvars.setdefault("ANSIBLE_HOST_KEY_CHECKING", "false")
    envvars.setdefault("ANSIBLE_FORCE_COLOR", "true")
    cmdline = " ".join(itertools.chain(ansible_extra_args or [], playbooks))
    if dry_run:
        cmdline += " -C"
    return ansible_runner.run(
        binary=os.path.join(virtualenv.virtualenv, "bin/ansible-playbook"),
        cmdline=cmdline,
        envvars=envvars,
        **kwargs
    )


def assert_ansible_error(run):
    assert run.status == "successful"
    assert len(re.findall(r".*fatal: .*", run.stdout.read())) == 0
    for host_failed, number_failed in run.stats.get("failures", {}).items():
        assert number_failed == 0
