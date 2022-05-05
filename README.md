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

[Variables reference](docs/variables.md)

## Tips and Tricks

[Tips&Tricks](tips_tricks.md)