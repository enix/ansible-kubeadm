import os

import vagrant


class LocalVagrant:
    def __init__(self, envs={}):
        self.vagrant = vagrant.Vagrant(quiet_stdout=False, quiet_stderr=False)
        std_envs = dict(os.environ)  # Inherit from current env, not reset it.
        std_envs.update(envs)
        std_envs.setdefault("SKIP_ANSIBLE", "true")
        self.vagrant.env = std_envs

    @property
    def vars(self):
        return VagrantVarSetter(self.vagrant)

    def init(self):
        pass

    def apply(self):
        self.vagrant.up()

    def cluster(self):
        return self

    @property
    def inventory(self):
        return os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            ".vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory",
        )

    def destroy(self):
        self.vagrant.destroy()


class VagrantVarSetter:
    def __init__(self, vagrant):
        self.vagrant = vagrant

    def __setitem__(self, variable, value):
        self.vagrant.env[variable.upper()] = value
