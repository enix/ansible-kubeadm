A plugin allow custom code to be run at key point (*a hook*) of the ansible_kubedm playbooks.
It comes with great possibilities, hence use with caution is required.

### Plugins

Plugins are discovered in `kubeadm_plugins_dir` which default to `{{ inventory_dir }}/kubeadm.plugins.d`.

Simply create a directory with the name of the plugin (whatever you like exept hidden one).

Inside this directory create a directory per *hook* name.

Finally put yaml with tasks list inside hook's directories.

**Note**: Those are *tasks* like in roles not *playbooks*.

Here is a sample layout, using the default settings for `kubeadm_plugins_dir`:

```
hosts.cfg # the inventory
group_vars/
host_vars/
kubeadm.plugins.d/
    upgrade_os/
        post_nodes_upgrade/          # Will be run on control plane and workers node when upgrade is launched
            subdir/
                clean_old_kernel.yml # will not be loaded, but could included
            upgrade_os.yml           # will be loaded
    .upgrade_cri/
        post_nodes_upgrade/
            cri_update.yml           # will not be loaded, because plugin name is an hidden directory
```

All the available hooks are listed bellow.

## Hooks

The following sections present each playbook workflow, hooks are marked with `[]`

Some hooks are present multiple times, so be careful choosing the hook name, when writing plugin.

#### 00-apiserver-proxy.yml

- find IP of control plane
- [pre_apiserver_proxy]
- deploy apiserver proxy
- [post_apiserver_proxy]

In case of running an upgrade to haproxy proxy loadbalancer (first on each control plane then all workers):

- [pre_proxy_upgrade_haproxy]
- Upgrade mechanism to haproxy
- [post_proxy_upgrade_haproxy]


#### 01_site.yml

The main body execute:

- [pre_run]
- Do some checks on control plane nodes
- [post_preflight_cp]
- Do some checks on worker nodes
- [post_preflight_nodes]
- Do some initialization tasks on control plane nodes
- [post_first_tasks_cp]

In case no cluster is found, will init one on a single control plane nodes:

- [pre_init]
- Init cluster
- [post_init]

Then continue some indempotent tasks on control plane nodes:

- [pre_config_update]
- Create bootstrap token if required
- Update kubeadm config
- [post_config_update]

In case an upgrade of kubernetes is required, run it now:

- [pre_kube_upgrade]
- Upgrade kubernetes
- [post_kube_upgrade]

Apply upgrade on control plane nodes (node by node by default):

- [pre_cp_upgrade, pre_nodes_upgrade]
- Apply upgrade on control plane nodes
- [post_cp_upgrades, post_nodes_upgrade]

Apply updade on worker nodes (node-by-node by default):

- [pre_workers_upgrade, pre_nodes_upgrade]
- Apply upgrade on worker nodes
- [post_workers_upgrade, post_nodes_upgrade]

Then join missing control plane nodes

- [pre_cp_join, pre_nodes_join]
- Join control plane nodes
- [post_cp_join, post_nodes_join]

Finally join missing workers nodes:

- [pre_workers_join, pre_nodes_join]
- Join worker nodes
- [post_workers_join, post_nodes_join]

Finally executing the last hook:

- [post_run]
