# To join worker-only nodes

**Note** : For control plane nodes, see dedicated [section](join_nodes.md#to-join-control-plane-nodes)

Let's assume that you have a cluster with two nodes and that you want to add a third node `node-3`
You can join multiple worker node at once with this procedure,

### Add node to the inventory

First, add the node to the inventory like the following inventory:

```
[kube_control_plane]
cp-1
cp-2
cp-3

[kube_workers]
node-1
node-2
node-3
```


### [optional] Deploy local apiserver proxy

If you don't have provision a load-balancer and require the local haproxy to be deployed:

```
ansible-playbook -i inventory enix.kubeadm.00_apiserver_proxy -e limit=nodes-3
```
You need to specify the `limit` variable via "extra-vars", because `-l` cannot really work in the context of ansible-kubeadm
(you need to connect to all the masters to get the IP needed to configure the loadbalancer)

### Joining nodes

You can join a node and skip other changes on other nodes by specify the limit variable.

```
ansible-play -i inventory.cfg enix.kubeadm.01_site -e limit=nodes-3
```



### Create bootstrap-token

Then create a bootstrap token by adding using the `bootstrap_token` tag.
Don't use a limit that skip control plane nodes.

```
ansible-playbook -i inventory.cfg enix.kubeadm.01_site -t bootstrap_token
```

No need to retrieve it by yourself, it will be discovered when joining the node
The token has a validity of 1H, so you don't need to repeat this step each time you try to join nodes

