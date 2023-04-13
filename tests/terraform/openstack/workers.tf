resource "openstack_compute_servergroup_v2" "workers_group" {
  name     = "${var.stem}-workers"
  policies = ["soft-anti-affinity"]
}

resource "openstack_compute_instance_v2" "workers" {
  name            = "${var.stem}-node-${count.index + 1}"
  image_name      = var.image_name
  flavor_name     = "GP1.S"
  key_pair        = openstack_compute_keypair_v2.ssh_deploy.name
  security_groups = ["default", openstack_compute_secgroup_v2.kubeadm.name]

  dynamic "network" {
    for_each = local.network_id_list
    content {
      uuid = network.value
    }
  }

  scheduler_hints {
    group = openstack_compute_servergroup_v2.workers_group.id
  }

  metadata = {
    "groups.enix.io" = "kube_workers"
  }

  count = var.worker_count
}

resource "openstack_networking_floatingip_v2" "floatip_workers" {
  pool = var.floating_pool

  count = var.worker_count
}

resource "openstack_compute_floatingip_associate_v2" "workers_pub_ip" {
  floating_ip = openstack_networking_floatingip_v2.floatip_workers[count.index].address
  instance_id = openstack_compute_instance_v2.workers[count.index].id

  count = var.worker_count
}

