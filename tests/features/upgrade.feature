Feature: Upgrade
    A test to upgrade a kubeadm cluster

    Scenario Outline: Upgrade via ansible-kubeadm
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
            kube_version: <from_version>
            action_reasons_review_skip: true
        When I run the playbook tests/playbooks/prepare.yml
        When I run the playbooks 00_apiserver_proxy.yml
                                 01_site.yml
        When I run the playbook tests/playbooks/cni.yml

        When With those group_vars on group all: kube_version: <to_version>
        When I run the playbooks 00_apiserver_proxy.yml
                                 01_site.yml

        Then I should have a working cluster

        Examples:
        | from_version | to_version |
        | 1.21         | 1.22       |
        | 1.23         | 1.24       |
