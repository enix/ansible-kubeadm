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
ansible-playbook -i inventory enix.kubeadm.00_apiserver_proxy -l kube_control_plane:nodes-3
```
You can skip the `-l` argument, if you're cluster doesn't have pending change you want to preserve on other nodes.
Don't forget to put all control_plane or it will fail to provision the apiserver proxy


### Create bootstrap-token

Then create a bootstrap token by adding using the `bootstrap_token` tag.
Don't use a limit that skip control plane nodes.

```
ansible-playbook -i inventory.cfg enix.kubeadm.01_site -t bootstrap_token
```

No need to retrieve it by yourself, it will be discovered when joining the node
The token has a validity of 1H, so you don't need to repeat this step each time you try to join nodes

### Joining nodes

You can join a node and skip other changes to the cluster by using the `join` tag.
With the tag, you can limit to hosts you want to join.

```
ansible-play -i inventory.cfg enix.kubeadm.01_site -t join -l nodes-3
```

## Alternative method

You can merge the creation of the boostrap token with the joining of the action of join:

```
ansible-playbook -i inventory.cfg enix.kubeadm.01_site -t bootstap_token,join -l kube_control_plane:node-3
```

Please note that you need to include a least one control plane node in the limit host pattern,
You can also skip the limit host pattern to apply to all nodes as those step are indempotent on their own: it will not mess with the current nodes.

# To join control-plane nodes

There is no tag for this operation, you need to apply the entire playbook for this
