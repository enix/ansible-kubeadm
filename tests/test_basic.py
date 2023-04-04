from pytest_bdd import scenario


@scenario("features/install.feature", "Install via ansible-kubeadm")
def test_install():
    pass


@scenario("features/upgrade.feature", "Upgrade via ansible-kubeadm")
def test_upgrade():
    pass


@scenario("features/haproxy.feature", "Test upgrade to haproxy pkg")
def test_haproxy():
    pass
