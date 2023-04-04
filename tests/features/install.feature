Feature: Install
    A test to install a kubeadm cluster from scratch

    Scenario: Install via ansible-kubeadm
        Given I want ansible 3
        Given Some running VMs

        When With those group_vars on group all:
            cluster_config:
             networking:
               podSubnet: 10.95.0.0/16
             controllerManager:
               extraArgs:
                 "allocate-node-cidrs": "true"
            cni: "kube-router"
            kubelet_config:
              cgroupDriver: "systemd"
            kube_version: 1.23
        When I run the playbook tests/playbooks/prepare.yml
        When I run ansible-kubeadm
        When I run the playbook tests/playbooks/cni.yml
        When I run the playbook tests/playbooks/verify.yml
        Then I should not see error message

        When I reset tasks counters
        And  I run ansible-kubeadm
        Then I should not see error message
        And  I should see no orange/yellow changed tasks
