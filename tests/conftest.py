import os
import fnmatch

import pytest

from tests.helpers.terraform import create_terraform


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def openstack_vms(anyio_backend):
    mounts = {}
    envs = {}
    ssh_pub = os.path.expanduser("~/.ssh/id_rsa.pub")
    if os.path.exists(os.path.expanduser("~/.ssh/id_rsa.pub")):
        mounts["/root/.ssh/id_rsa.pub"] = ssh_pub
    clouds_yaml = os.path.expanduser(
        os.environ.get("OS_CLIENT_CONFIG_FILE", "~/.config/openstack/clouds.yaml")
    )
    if os.path.exists(clouds_yaml):
        mounts["/root/.config/openstack/clouds.yaml"] = clouds_yaml
    for name, value in os.environ.items():
        if fnmatch.fnmatch(name, "OS_*"):
            envs[name] = value
    async with create_terraform(
        tfdata_dir="./tests/terraform", mounts=mounts, envs=envs
    ) as tf:
        await tf.init().stdout()
        await tf.apply().stdout()
        if os.environ.get("TERRAFORM_KEEP", "false").lower() not in ["true", "1"]:
            await tf.destroy().stdout()
