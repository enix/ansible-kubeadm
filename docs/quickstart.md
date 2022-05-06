### Install ansible-kubeadm an

```
ansible-galaxy collection install git+ssh://git@github.com/enix/ansible-kubeadm
```

Also install docker so we can have container running ^^
```
ansible-galaxy install geerlingguy.docker
```

### Prepare inventory

create an inventory like this

```
[kube_control_plane]
kubeadm-cp-01   ansible_host=ip-cp1
kubeadm-cp-02   ansible_host=ip-cp2
kubeadm-cp-03   ansible_host=ip-cp3

[kube_workers]
kubeadm-node-01 ansible_host=ip-no1
# ... more nodes

[all:vars]
ansible_user=ubuntu
ansible_become=true
```

### Run

```
ansible -i hosts -m include_role -a"name=geerlingguy.docker" -e 'docker_daemon_options={"exec-opts"=["native.cgroupdriver=systemd"]}'
ansible-playbook -i hosts enix.kubeadm.00_apiserver_proxy.yml enix.kubeadm.01_site.yml
```

You can customize install by adding group_vars, following [Variables references](variables.md)