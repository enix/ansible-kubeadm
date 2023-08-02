import json
import re
import subprocess
import typing


class TerraformCompose:
    KNOWN_OS = {}

    def __init__(
        self,
        tfdata_dir: str = ".",
        service_name: str = "terraform",
        compose_file: typing.Optional[str] = None,
        envs: dict = {},
        mounts: dict = {},
        version: typing.Optional[str] = None,
    ):
        self.tfdata_dir = tfdata_dir
        self.service_name = service_name
        self.compose_file = compose_file
        self.envs = envs
        self.mounts = mounts
        self.version = version
        self._operating_system = None

    @property
    def base_command(self):
        command = ["docker", "compose"]
        if self.compose_file:
            command += ["-f", self.compose_file]
        command += ["run"]
        for key, value in self.envs.items():
            command += ["-e", "{}={}".format(key, value)]
        for src, dest in self.mounts.items():
            command += ["-v", "{}:{}".format(src, dest)]
        if self.version:
            command += ["-e", "TERRAFORM_VERSION={}".format(self.version)]
        if self.tfdata_dir != ".":
            command += ["-w", self.tfdata_dir]
        command += [self.service_name]
        return command

    @property
    def vars(self):
        return VarSetter(self.envs)

    @property
    def operating_system(self):
        return self._operating_system

    @operating_system.setter
    def operating_system(self, operating_system):
        formated_name = " ".join(re.findall(r"([a-zA-Z]+|[-\d.]+)", operating_system))
        self.vars["image_name"] = self.KNOWN_OS.get(operating_system, formated_name)
        self._operating_system = operating_system

    def init(self):
        return subprocess.check_call(self.base_command + ["init"])

    def apply(self):
        return subprocess.check_call(self.base_command + ["apply", "-auto-approve"])

    def cluster(self):
        return self

    def output(self):
        return json.loads(
            subprocess.check_output(self.base_command + ["output", "-json"])
        )

    @property
    def inventory(self):
        return self.output()["inventory"]["value"]

    def destroy(self):
        return subprocess.check_call(self.base_command + ["destroy", "-auto-approve"])


class VarSetter:
    def __init__(self, envs):
        self.envs = envs

    def __setitem__(self, variable, value):
        self.envs["TF_VAR_{}".format(variable)] = value
