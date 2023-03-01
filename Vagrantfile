CONTROL_PLANE_COUNT = (ENV['CONTROL_PLANE_COUNT'] || 2).to_i
WORKER_COUNT = (ENV['WORKER_COUNT'] || 1).to_i
SKIP_ANSIBLE = ENV['SKIP_ANSIBLE'] || false
BOX_IMAGE = ENV['BOX_IMAGE'] || "generic/ubuntu2004"

Vagrant.configure("2") do |config|
    config.vm.box = BOX_IMAGE

    (1..CONTROL_PLANE_COUNT).each do |i|
        config.vm.define "control-plane-#{i}" do |node|
            node.vm.hostname = "control-plane-#{i}"
            node.vm.synced_folder ".", "/vagrant", disabled: true
            if ENV['NETWORK_SWITCH']
                node.vm.network "public_network", bridge: ENV['NETWORK_SWITCH']
            end
        end
    end
    (1..WORKER_COUNT).each do |i|
        config.vm.define "worker-#{i}" do |node|
            node.vm.hostname = "worker-#{i}"
            node.vm.synced_folder ".", "/vagrant", disabled: true
            if ENV['NETWORK_SWITCH']
                node.vm.network "public_network", bridge: ENV['NETWORK_SWITCH']
            end
            if i == WORKER_COUNT
                groups = {
                  "kube_control_plane" => (1..CONTROL_PLANE_COUNT).map{|i| "control-plane-#{i}"},
                  "kube_workers" => (1..WORKER_COUNT).map{|i| "worker-#{i}"},
                  "kube:children" => ["kube_control_plane", "kube_workers"],
                  "kube:vars" => {
                        "ansible_ssh_pipelining" => true,
                        "ansible_become" => true,
                  }
                }
                node.vm.provision "ansible" do |inventory|
                    inventory.playbook = "tests/playbooks/prepare.yml"
                    inventory.limit = "all"
                    inventory.skip_tags = "always,all"
                    inventory.groups = groups
                end
                if not SKIP_ANSIBLE
                    groups["kube:vars"].update({
                      "kubelet_config" => '{"cgroupDriver": "systemd"}',
                      "apiserver_proxy_use_docker" => false,
                      "control_plane_endpoint" => "127.0.0.1:7443",
                      "kube_version" => ENV['KUBE_VERSION'] || "1.23",
                    })
                    node.vm.provision "ansible" do |prepare|
                        prepare.playbook = "tests/playbooks/prepare.yml"
                        prepare.limit = "all"
                        prepare.groups = groups
                    end
                    node.vm.provision "ansible" do |proxy|
                        proxy.playbook = "playbooks/00_apiserver_proxy.yml"
                        proxy.limit = "all"
                        proxy.groups = groups
                    end
                    node.vm.provision "ansible" do |kubeadm|
                        kubeadm.playbook = "playbooks/01_site.yml"
                        kubeadm.limit = "all"
                        kubeadm.groups = groups
                    end
                end
            end
        end
    end
end

