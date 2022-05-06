User facing variables:

| name                              | scope               | default                     | usage                                                                 |
|-----------------------------------|---------------------|-----------------------------|-----------------------------------------------------------------------|
| enable_kubeadm_patches            | control plane       | true                        | Deploy patches and pass `kubeadm_patch_dir` to kubeadm so that patch are applied         |
| kube_cp_group                     | playbook invocation | "kube_control_plane"        | name of the ansible group for install control plane nodes             |
| kube_worker_group                 | playbook invocation | "kube_workers"              | name of the ansible group for installing pure worker nodes            |
| kube_control_plane_cidr           | control plane       | "" (let kubeadm default)    | CIDR (eg "192.168.99.0/24") filter addresses for `_etcd_metrics_bind_address`, `_kube_apiserver_advertise_address`, `_kube_controller_manager_bind_address`, `_kube_scheduler_bind_address`|
| kube_apiserver_advertise_cidr     | control plane       | "" (let kubeadm default)    | CIDR (eg "192.168.99.0/24") filter the advertise address to `_kube_apiserver_advertise_address` (override `kube_control_plane_cidr`) |
| kube_controller_manager_bind_cidr | control plane       | "" (let kubeadm default)    | CIDR (eg "192.168.99.0/24") filter the bind address for `_kube_controller_manager_bind_address` (override `kube_control_plane_cidr`)|
| kube_scheduler_bind_cidr          | control plane       | "" (let kubeadm default)    | CIDR (eg "192.168.99.0/24") filter the bind address for `_kube_scheduler_bind_address` (override `kube_control_plane_cidr`)|
| kubeadm_extra_patches             | control plane       | {}                          | dictionnary containing extra kubeadm patches to deploy (key = "filename", value = "patch to template") |
| kubeadm_patch_dir                 | control plane       | "/etc/kubeadm/directory"    | directory containing patch for kubeadm                                |
| kubeadm_patch_owner               | control plane       | "root"                      | owner of the patches created in `kubeadm_patch_dir`                   |
| kubeadm_patch_group               | control plane       | "root"                      | group of the patched created in `kubeadm_patch_dir`                   |
| kubeadm_patch_mode                | control plane       | "0750"                      | permission mode of the patches created in `kubeadm_patch_dir`         |
| kubeadm_patch_dir_owner           | control plane       | "{{ kubeadm_patch_owner }}" | owner of the directory `kubeadm_patch_dir`                            |
| kubeadm_patch_dir_group           | control plane       | "{{ kubeadm_patch_group }}" | group of the directory `kubeadm_patch_dir`                            |
| kubeadm_patch_dir_mode            | control plane       | "0750"                      | permission mode of the directory `kubeadm_patch_dir`                  |
| kubelet_node_cidr                 | control plane       | "" (let kubeadm default)    | CIDR (eg "192.168.99.0/24") filter the address for `_kubelet_node_ip` |
| upgrade_cp_serial                 | playbook invocation | "1"                         | Specify ansible batch size (https://docs.ansible.com/ansible/latest/user_guide/playbooks_strategies.html#setting-the-batch-size-with-serial) during control plane nodes upgrade phase. Default to 1 (1 node at a time) |
| upgrade_worker_serial             | playbook invocation | "1"                         | Specify ansible batch size (https://docs.ansible.com/ansible/latest/user_guide/playbooks_strategies.html#setting-the-batch-size-with-serial) during pure worker nodes upgrade phase. Defaul to 1 (1 node at a time )   |

Internal variables:

| name                                  | scope               | default                  | usage                                              |
|---------------------------------------|---------------------|--------------------------|----------------------------------------------------|
| _control_plane                        | roles               | false                    | trigger control_plane fonction of various roles (join_nodes, find_ip, packages)                       |
| _etcd_metrics_bind_address            | roles               |                          | Make etcd bind the `_etcd_metrics_bind_address` to expose prometheus metrics                          |
| _kube_apiserver_advertise_address     | roles               |                          | Interface object|
| _kube_controller_manager_bind_address | roles               |                          | Interface object|
| _kube_scheduler_bind_address          | roles               |                          | Interface object|
| _kubelet_node_ip                      | roles               |                          | Interface object|
