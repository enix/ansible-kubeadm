import os

import pytest
import tenacity


@pytest.fixture
def provider(request):
    if os.environ.get("OS_CLOUD") is not None:
        provider = "openstack"
    else:
        raise RuntimeError("Openstack EnvVar cannot be found")
    return request.getfixturevalue(provider)


@tenacity.retry(reraise=True, stop=tenacity.stop_after_attempt(2))
def cluster_spawn(provider):
    provider.init()
    provider.apply()


@pytest.fixture
def cluster(request, provider):
    try:
        cluster_spawn(provider)
        yield provider.cluster()
        if not request.config.getoption("keep_servers"):
            provider.destroy()
    except Exception:
        if not request.config.getoption("keep_servers_after_fail"):
            provider.destroy()
