resource "openstack_compute_servergroup_v2" "cp_group" {
  name     = "${var.stem}-cp"
  policies = ["soft-anti-affinity"]
}

resource "openstack_compute_instance_v2" "control_plane" {
  name            = "${var.stem}-cp-${count.index + 1}"
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
    group = openstack_compute_servergroup_v2.cp_group.id
  }

  metadata = {
    "groups.enix.io" = "kube_control_plane"
  }

  count = var.control_plane_count
}

resource "openstack_networking_floatingip_v2" "floatip_cp" {
  pool = var.floating_pool

  count = var.control_plane_count
}

resource "openstack_compute_floatingip_associate_v2" "cp_pub_ip" {
  floating_ip = openstack_networking_floatingip_v2.floatip_cp[count.index].address
  instance_id = openstack_compute_instance_v2.control_plane[count.index].id

  count = var.control_plane_count
}
