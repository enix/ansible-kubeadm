# ansible-kubeadm

Aims to manage kubeadm based cluster via ansible

What ansible-kubeadm can do:
  - Install kubeadm on a variety of linux distribution
  - lock kubeadm package to avoid upgrade
  - init a cluster and join node in a idempotent manner
  - upgrade a cluster in an indempotent maner (just add +1 to minor version config and your good to go !)

What ansible-kubeadm expect to be done and will not do:
  - Upgrading distro
  - Upgrade the kernel
  - install ntp
  - installing docker (or whatever CRI)
  - disable swap
  - remove unattented-upgrade
  - configure CNI

## Quickstart

see [Quickstart](docs/quickstart.md)

## Configuration

If you want a customized (ansible-)kubeadm experience there is a number of variables you can use:

## Migration planning

Long term migration plan, [*] to indicate current phase

| Reason                                               | Phase 1                                                                                                            | Phase 2                                                         | Phase 3              |
|------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|----------------------|
| Docker has been deprecated in kubernetes since 1.24+ | [*] haproxy pkg used by default for proxy. Able to install compose-based proxy. Migration from compose to pkg possible | Not able to install compose-based proxy. Migration possible | Migration phased out |


[Variables reference](docs/variables.md)

## Tips and Tricks

[Tips&Tricks](tips_tricks.md)
