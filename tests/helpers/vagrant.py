import os
import shutil

import vagrant


class LocalVagrant:
    KNOWN_OS = {}

    def __init__(self, envs={}, inventory_dir_copy=None):
        self.vagrant = vagrant.Vagrant(quiet_stdout=False, quiet_stderr=False)
        std_envs = dict(os.environ)  # Inherit from current env, not reset it.
        std_envs.update(envs)
        std_envs.setdefault("SKIP_ANSIBLE", "true")
        self.inventory_dir_copy = inventory_dir_copy
        self.vagrant.env = std_envs
        self._operating_system = None

    @property
    def operating_system(self):
        return self._operating_system

    @operating_system.setter
    def operating_system(self, operating_system):
        self.vars["BOX_IMAGE"] = self.KNOWN_OS.get(
            operating_system, "generic/{}".format(operating_system)
        )
        self._operating_system = operating_system

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
    def vagrant_inventory(self):
        return os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            ".vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory",
        )

    @property
    def inventory(self):
        # give a fresh dir each time, to add group vars
        if self.inventory_dir_copy:
            new_inventory = os.path.join(self.inventory_dir_copy, "vagrant.cfg")
            shutil.copyfile(self.vagrant_inventory, new_inventory)
            return new_inventory
        else:
            return self.vagrant_inventory

    def destroy(self):
        self.vagrant.destroy()


class VagrantVarSetter:
    def __init__(self, vagrant):
        self.vagrant = vagrant

    def __setitem__(self, variable, value):
        self.vagrant.env[variable.upper()] = value
