#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fnmatch

from ansible.module_utils.basic import AnsibleModule

try:
    import apt
    HAS_APT = True
except ImportError:
    HAS_APT = False


class PkgVersionMatch(object):

    def __init__(self, name, version=None):
        self.name = name
        self.version = version

    def execute(self):
        if HAS_APT:
            version = self.find_apt()
        return {'version': version}

    def find_apt(self):
        cache = apt.Cache()
        try:
            pkg = cache[self.name]
        except KeyError:
            raise PkgVersionMatchError(
                "package '{}' cannot be found in database".format(self.name)
            )
        if not self.version:
            return pkg.candidate.version
        if '*' in self.version:
            match_version = self.version
        else:
            match_version = '{}*'.format(self.version)
        for version in pkg.versions:
            if fnmatch.fnmatch(version.version, match_version):
                return version.version
        raise PkgVersionMatchError(
            "Can't found matching version '{}' of package '{}' in database".format(
                self.name, self.version)
        )


class PkgVersionMatchError(Exception):
    """Error from PkgVersionMatch Module"""


class PkgVersionMatchAnsible(AnsibleModule, PkgVersionMatch):

    def __init__(self, *args, **kwargs):
        AnsibleModule.__init__(
            self,
            argument_spec=dict(
                name=dict(required=True, type='str'),
                version=dict(required=False, type='str', default=None)
            ),
            supports_check_mode=True,
        )
        if not HAS_APT:
            self.fail_json(msg='Install python-apt')
        PkgVersionMatch.__init__(self, **self.params)


def main():
    module = PkgVersionMatchAnsible()
    try:
        res_dict = module.execute()
    except PkgVersionMatchError as exc:
        module.fail_json(msg=exc.args[0])
    else:
        module.exit_json(**res_dict)


if __name__ == '__main__':
    main()
