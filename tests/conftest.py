# flake8: noqa: F811
import argparse
import os
import re

import pytest
import tenacity
import yaml
from pytest_bdd import given, parsers, then, when

from tests.helpers.ansible import (
    assert_ansible_error,
    install_ansible,
    install_galaxy_deps,
    run_ansible_playbook,
)
from tests.helpers.provider import cluster, provider  # noqa: F401, Those are fixtures
from tests.helpers.terraform import TerraformCompose
from tests.helpers.vagrant import LocalVagrant

DEFAULT_OS = ["ubuntu2204"]
ALL_OS = ["ubuntu2004", "ubuntu2204", "debian11"]


def pytest_addoption(parser):
    TRUE_VALUES = ["true", "yes", "y", "1"]
    parser.addoption(
        "--keep-servers",
        dest="keep_servers",
        nargs="?",
        type=bool,
        const=True,
        default=os.environ.get("KEEP_SERVERS", "false").lower() in TRUE_VALUES,
    )
    parser.addoption(
        "--keep-servers-after-fail",
        dest="keep_servers_after_fail",
        nargs="?",
        type=bool,
        const=True,
        default=os.environ.get("KEEP_SERVERS_AFTER_FAIL", "true").lower()
        in TRUE_VALUES,
    )
    parser.addoption(
        "--all-os",
        dest="os_list",
        action="store_const",
        const=ALL_OS,
        help="Run tests on all known OS",
    )
    parser.addoption(
        "-O",
        "--os",
        dest="os_list",
        nargs="+",
        action="extend",
        default=[],
        help="Select OS to run tests on",
    )
    parser.addoption(
        "-A",
        "--ansible",
        dest="ansible_extra_args",
        nargs=argparse.REMAINDER,
        help="Ansible extra args",
    )


def pytest_generate_tests(metafunc):
    if "operating_system" in metafunc.fixturenames:
        metafunc.parametrize(
            "operating_system",
            metafunc.config.getoption("os_list") or DEFAULT_OS,
            indirect=True,
        )


@pytest.fixture
def operating_system(request, provider):
    provider.operating_system = request.param


@pytest.fixture
def openstack(tmp_path):
    return TerraformCompose(
        envs={"TF_VAR_inventory_dir": tmp_path},
        mounts={tmp_path: tmp_path},
    )


@pytest.fixture
def vagrant(tmpdir):
    return LocalVagrant(inventory_dir_copy=tmpdir)


@then("Set cluster {variable}={value}")
@given("The cluster {variable)={value}")
def cluster_set_param(provider, variable, value):
    provider.vars[variable] = value
    # Refresh infrastructure
    provider.apply()


@pytest.fixture
def ansible(virtualenv):
    install_ansible(virtualenv)


@given(parsers.parse("I want ansible {version}"), target_fixture="ansible")
def ansible_with_version(virtualenv, version):
    install_ansible(virtualenv, version)


@pytest.fixture
def galaxy_deps(ansible, virtualenv):
    install_galaxy_deps(virtualenv)


@given("Some running VMs", target_fixture="inventory")
def inventory(cluster):
    return cluster.inventory


@when(
    parsers.re(
        r"With those group_vars on group (?P<group>[\w-]+):\s*(?P<vars_snippet>.*)",
        re.DOTALL,
    )
)
def group_vars(inventory, group, vars_snippet):
    group_vars_dir = os.path.join(os.path.dirname(inventory), "group_vars")
    try:
        os.makedirs(group_vars_dir)
    except FileExistsError:
        if not os.path.isdir(group_vars_dir):
            raise
    group_vars_file = os.path.join(group_vars_dir, "{}.yml".format(group))
    try:
        with open(group_vars_file) as fd:
            group_vars = yaml.safe_load(fd)
    except FileNotFoundError:
        group_vars = {}
    vars_dict = yaml.safe_load(vars_snippet)
    group_vars.update(vars_dict)
    with open(group_vars_file, "w+") as fd:
        fd.write(yaml.dump(group_vars))


@pytest.fixture()
def results():
    return {}


@pytest.fixture
def ansible_extra_args(request):
    return request.config.getoption("ansible_extra_args")


@when(
    parsers.re(
        r"I (?P<dry_run>dry-)?run the playbooks?:?\s+(?P<playbooks>.+?)(?P<with_err>\s+with error:?\s+)?(?(with_err)(?P<error>.+)|\Z)",
        re.DOTALL,
    )
)
@tenacity.retry(reraise=True, stop=tenacity.stop_after_attempt(2))
def ansible_playbook(
    inventory,
    virtualenv,
    galaxy_deps,
    ansible_extra_args,
    results,
    playbooks,
    dry_run,
    error,
):
    if dry_run == "dry-":
        dry_run = True
    else:
        dry_run = False
    playbook_list = re.findall(r"[\w./]+", playbooks)
    if not all(os.path.exists(p) for p in playbook_list):
        playbook_list_subdir = [os.path.join("playbooks", p) for p in playbook_list]
        if all(os.path.exists(p) for p in playbook_list_subdir):
            playbook_list = playbook_list_subdir
        else:
            raise ValueError("All playbooks could not be found")
    result = run_ansible_playbook(
        virtualenv,
        playbook_list,
        ansible_extra_args=ansible_extra_args,
        inventory=inventory,
        dry_run=dry_run,
    )
    if error:
        assert result.status == "failed"
        assert error.strip() in result.stdout.read()
    else:
        assert_ansible_error(result)
    results.setdefault("ansible_run", []).append(result)


@then("I should have a working cluster")
@tenacity.retry(reraise=True, stop=tenacity.stop_after_attempt(2))
def ansible_kubeadm(inventory, virtualenv, galaxy_deps, ansible_extra_args, results):
    result = run_ansible_playbook(
        virtualenv,
        ["tests/playbooks/verify.yml"],
        ansible_extra_args=ansible_extra_args,
        inventory=inventory,
    )
    assert_ansible_error(result)


@when("I reset tasks counters")
def reset_counter(results):
    results["ansible_run"] = []


@then("I should see no orange/yellow changed tasks")
def check_changed_tasks(results):
    for run in results["ansible_run"]:
        for host_changed, number_changed in run.stats.get("changed", {}).items():
            assert number_changed == 0
