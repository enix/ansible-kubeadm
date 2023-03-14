Feature: Install
    A test to install a kubeadm cluster from scratch

    Scenario: Install via ansible-kubeadm
        Given I want ansible 3
        Given Some running VMs

        When With those group_vars on group all:
            kubelet_config:
              cgroupDriver: "systemd"
            apiserver_proxy_use_docker: false
            kube_version: 1.23
        When I run the playbook tests/playbooks/prepare.yml
        When I run ansible-kubeadm
        Then I should not see error message

        When I reset tasks counters
        And  I run ansible-kubeadm
        Then I should not see error message
        And  I should see no orange/yellow changed tasks
