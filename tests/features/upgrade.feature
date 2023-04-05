Feature: Upgrade
    A test to upgrade a kubeadm cluster

    Scenario: Upgrade via ansible-kubeadm
        Given I want ansible 3
        Given Some running VMs

        When With those group_vars on group all:
             cluster_config:
               networking:
                 podSubnet: 10.95.0.0/16
               controllerManager:
                 extraArgs:
                   "allocate-node-cidrs": "true"
            kubelet_config:
              cgroupDriver: "systemd"
            apiserver_proxy_use_docker: false
            kube_version: 1.23
        When I run the playbook tests/playbooks/prepare.yml
        When I run ansible-kubeadm
        When I run the playbook tests/playbooks/cni.yml
        Then I should not see error message

        When With those group_vars on group all: kube_version: 1.24
        And  I run ansible-kubeadm
        When I run the playbook tests/playbooks/verify.yml
        Then I should not see error message
