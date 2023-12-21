
Hidden (and less stable feature), tips and tricks

### No inventory ? No problem !

```
ansible-playbook -i <on_master_ip_look_at_comma_after>, -b -k -u admin playbooks/00_inventory.yml playbooks/01_site.yml
```


### You have openstack, you want a cluster real quick ?

```
export OS_CLOUD=openstack  # and any other openstack environment variable
docker compose run dev -e kube_version=1.25
```

A bit of explanations:

  - standard pytest argument `-k` to select the `install` test that does only install ansible-kubeadm
  - `--keep-servers` custom argument to keep servers after the test (default to False)
  - `-A` custom argument to pass any remaining arguments to ansible (here customize the version of kubernetes to install)

To tear down manually when you finished

```
export OS_CLOUD=openstack
docker compose run terraform destroy
```

**NOTE**: for mac os users, please add `_SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock` in a `.env` file at the top level directory of the repository
