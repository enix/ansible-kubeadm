# ansible-kubeadm

Aims to manage kubeadm based cluster via ansible

Should be done before:
  - Upgrading distro
  - install ntp
  - installing docker (or whatever CRI)
  - disable swap
  - remove unattented-upgrade

## How-To

### Prepare inventory

create an inventory like this

```
[kube_control_plane]
kubeadm-cp-01   ansible_host=ip-cp1
kubeadm-cp-02   ansible_host=ip-cp2
kubeadm-cp-03   ansible_host=ip-cp3

[kube_nodes]
kubeadm-node-01 ansible_host=ip-no1
# ... more nodes

[all:vars]
ansible_user=ubuntu
ansible_become=true
```

### Install ansible-kubeadm

THIS IS NOT YET SUPPORTED BY ANSIBLE ([merged in ansible 2.10](https://github.com/ansible/ansible/pull/69154))
```
ansible-galaxy collection install git+ssh://git@gitlab.enix.io/kubernetes/ansible-kubeadm
```

### Run

```
ansible-playbook -i hosts ansible-kubeadm/playbooks/00-site.yaml
```
