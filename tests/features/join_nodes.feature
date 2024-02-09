Feature: Upgrade
    A test to upgrade a kubeadm cluster

    Scenario: Upgrade via ansible-kubeadm
        Given I want ansible 3
        Given The cluster control_plane_count = 1
        Given The cluster worker_count = 1
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
            kube_version: 1.23
        When I run the playbook tests/playbooks/prepare.yml
        When I run the playbooks 00_apiserver_proxy.yml
                                 01_site.yml
        When I run the playbook tests/playbooks/cni.yml

        Then Set cluster worker_count = 2

        When With those group_vars on group all: kube_version: 1.24
        When I run the playbooks 00_apiserver_proxy.yml
                                 01_site.yml

        Then I should have a working cluster
