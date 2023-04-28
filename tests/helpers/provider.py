import os
from typing import Dict

import pytest
import tenacity
from pytest import CollectReport, StashKey

# https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures
phase_report_key = StashKey[Dict[str, CollectReport]]()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # store test results for each phase of a call, which can
    # be "setup", "call", "teardown"
    item.stash.setdefault(phase_report_key, {})[rep.when] = rep


@pytest.fixture
def provider(request):
    if os.environ.get("OS_CLOUD") is not None:
        provider = "openstack"
    else:
        provider = "vagrant"
        # raise RuntimeError("Openstack EnvVar cannot be found")
    return request.getfixturevalue(provider)


@tenacity.retry(reraise=True, stop=tenacity.stop_after_attempt(2))
def cluster_spawn(provider):
    provider.init()
    provider.apply()


@pytest.fixture
def cluster(request, provider, operating_system):
    keep_after_fail = request.config.getoption("keep_servers_after_fail")
    try:
        cluster_spawn(provider)
        yield provider.cluster()
        report = request.node.stash[phase_report_key]
        if "call" in report and report["call"].failed:
            if not keep_after_fail:
                provider.destroy()
        elif not request.config.getoption("keep_servers"):
            provider.destroy()
    except Exception:
        if not keep_after_fail:
            provider.destroy()
