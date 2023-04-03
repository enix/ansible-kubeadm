Hooks allow custom code to be run at key point of the ansible_kubeadm playbooks.
It comes with great possibilities, hence use with caution is required.

### Using hooks

Hooks are discovered in `kubeadm_hooks_dir` which default to `{{ inventory_dir }}`
Simply create a `kubeadm.<hook_name>.d` directory and puts tasks yaml files in it.

Note: Those are *tasks* like in roles not *playbooks*.

you can register you're `tasks` files by using the variable `kubeadm_hooks_<hook_name>`.

All the available hooks are listed bellow.

### playbooks

The following sections present each playbook workflow, hooks are markes with `[]`

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

- [pre_cp_upgrade]
- Apply upgrade on control plane nodes
- [post_cp_upgrades]

Apply updade on worker nodes (node-by-node by default):

- [pre_workers_upgrade]
- Apply upgrade on worker nodes
- [post_workers_upgrade]

Then join missing control plane nodes

- [pre_cp_join]
- Join control plane nodes
- [post_cp_join]

Finally join missing workers nodes:

- [pre_workers_join]
- Join worker nodes
- [post_workers_join]

Finally executing the last hook:

- [post_run]
