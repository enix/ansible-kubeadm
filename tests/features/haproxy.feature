Feature: Haproxy
    A test to migrate from compose to haproxy

    Scenario: Test upgrade to haproxy pkg
        Given I want ansible 3
        Given Some running VMs

        When With those group_vars on group all:
            cri_name: docker
            cluster_config:
              networking:
                podSubnet: 10.95.0.0/16
              controllerManager:
                extraArgs:
                  "allocate-node-cidrs": "true"
            kubelet_config:
              cgroupDriver: "systemd"
            apiserver_proxy_use_docker: true
            kube_version: 1.23
        When I run the playbook tests/playbooks/prepare.yml
        When I run the playbooks 00_apiserver_proxy.yml
                                 01_site.yml
        When I run the playbook tests/playbooks/cni.yml
        Then I should have a working cluster


        When With those group_vars on group all:
            apiserver_proxy_use_docker:
        When I reset tasks counters
        When I run the playbooks 00_apiserver_proxy.yml
                                 01_site.yml
             with error:
               As docker has been deprecated

        When With those group_vars on group all:
            apiserver_proxy_use_docker: false
        When I reset tasks counters
        When I run the playbooks 00_apiserver_proxy.yml
                                 01_site.yml
        Then I should have a working cluster
