"""
Execute a command
"""

import os
import stat
import sys
import anyio
import dagger

import contextlib
#import pytest

#pytestmark = pytest.mark.anyio


#@pytest.fixture
#def dagger_client():
#    config = dagger.Config(log_output=sys.stderr)
#    with dagger.Connection(config) as client:
#        yield client
#
#
#@pytest.fixture
#def terraform_image(dagger_client, version: str = "1.3.6"):
#    yield dagger_client.container().from_("hashicorp/terraform:{}".format(version))
#
#
#@pytest.fixture
#def tfdata_dir(dagger_client):
#    return dagger_client.host().directory("./tests/terraform")
#
#
#def terraform_run(image, tfdata_dir, mount_dirs, cmd):
#    return (
#        image.with_directory("/src", tfdata_dir, exclude=[]) # Exclude .git and .tox, but for now, it's buggy
#        .with_workdir("/src")
#        .with_exec(cmd)
#    )
#
#
#@pytest.fixture
#async def terraform_init(terraform_image, tfdata_dir):
#    result_init = terraform_run(terraform_image, tfdata_dir, ["init"]).stdout()
#    return result_init
#
#
#@pytest.fixture
#async def terraform_apply(terraform_image, terraform_init, tfdata_dir):
#    result_apply = terraform_run(
#        terraform_image, tfdata_dir, ["apply", "-auto-approve"]
#    ).stdout()
#    return result_apply


class TerraformContainer:

    def __init__(self, dagger_client, tfdata_dir: str='.', mounts: dict={}, envs: dict={}, version: str="1.3.6"):
        container = (
            dagger_client.container().from_(f"hashicorp/terraform:{version}")
            .with_directory("/src", dagger_client.host().directory(tfdata_dir))
            .with_workdir("/src")
        )
        for src, dest in mounts.items():
            if not os.path.exists(dest):
                raise OSError(f"file not found {dest}")
            stats = os.stat(dest).st_mode
            if stat.S_ISDIR(stats):
                container = container.with_directory(src, dagger_client.host().directory(dest))
            else:
                directory = dagger_client.host().directory(os.path.dirname(dest))
                container = container.with_file(src, directory.file(os.path.basename(dest)))
        for name, value in envs.items():
            container = container.with_env_variable(name, value)
        self.container = container


    def init(self):
        return self.container.with_exec(['init'])

    def apply(self):
        return self.container.with_exec(['apply', '-auto-approve'])

    def destroy(self):
        return self.container.with_exec(['destroy', '-auto-approve'])


@contextlib.asynccontextmanager
async def create_terraform(*args, **kwargs):
    config = dagger.Config(log_output=sys.stderr)
    async with dagger.Connection(config) as client:
        yield TerraformContainer(client, *args, **kwargs)
