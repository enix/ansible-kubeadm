from pytest_bdd import scenario

# In order for parametrization on operating_system to work, we need to have fixture
# directly called by the test function


@scenario("features/install.feature", "Install via ansible-kubeadm")
def test_install(operating_system):
    pass


@scenario("features/upgrade.feature", "Upgrade via ansible-kubeadm")
def test_upgrade(operating_system):
    pass


@scenario("features/haproxy.feature", "Test upgrade to haproxy pkg")
def test_haproxy(operating_system):
    pass


@scenario("features/join_nodes.feature", "Join nodes via ansible-kubeadm")
def test_join_nodes(operating_system):
    pass
