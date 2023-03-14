from pytest_bdd import scenario


@scenario("features/install.feature", "Install via ansible-kubeadm")
def test_install():
    pass


@scenario("features/upgrade.feature", "Upgrade via ansible-kubeadm")
def test_upgrade():
    pass
