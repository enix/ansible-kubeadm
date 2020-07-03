resource "openstack_compute_servergroup_v2" "node_group" {
  name     = "${var.stem}-nodes"
  policies = ["soft-anti-affinity"]
}

resource "openstack_compute_instance_v2" "nodes" {
  name            = "${var.stem}-node-${count.index + 1}"
  image_name      = var.image_name
  flavor_name     = "GP1.S"
  key_pair        = openstack_compute_keypair_v2.ssh_deploy.name
  security_groups = ["default", "${openstack_compute_secgroup_v2.kubeadm.name}"]

  network {
    uuid = data.openstack_networking_network_v2.network.id
  }

  scheduler_hints {
      group = openstack_compute_servergroup_v2.node_group.id
  }

  metadata = {
    "groups.enix.io" = "kube_nodes"
  }

  count = var.node_count
}

resource "openstack_networking_floatingip_v2" "floatip_nodes" {
  pool = var.floating_pool

  count = var.node_count
}

resource "openstack_compute_floatingip_associate_v2" "nodes_pub_ip" {
  floating_ip = openstack_networking_floatingip_v2.floatip_nodes[count.index].address
  instance_id = openstack_compute_instance_v2.nodes[count.index].id

  count = var.node_count
}

