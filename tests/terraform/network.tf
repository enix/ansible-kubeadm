data "openstack_networking_network_v2" "network" {
  name = var.network_name
}

resource "openstack_compute_secgroup_v2" "kubeadm" {
  name        = var.stem
  description = "Interconnection for cluster + ssh"

  rule {
    from_port   = 22
    to_port     = 22
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 1
    to_port     = 65535
    ip_protocol = "tcp"
    self        = true
  }

  rule {
    from_port   = 1
    to_port     = 65535
    ip_protocol = "udp"
    self        = true
  }
}

resource "openstack_networking_network_v2" "private_net" {
  name        = var.stem
  description = "private network"
  count       = var.allocate_private_net == true ? 1 : 0
}

resource "openstack_networking_subnet_v2" "private_subnet" {
  name       = var.stem
  network_id = openstack_networking_network_v2.private_net[0].id
  cidr       = var.private_subnet
  ip_version = 4
  count      = var.allocate_private_net == true ? 1 : 0
}

locals {
  network_id_list = compact([
    data.openstack_networking_network_v2.network.id,
    var.allocate_private_net == true ? openstack_networking_network_v2.private_net[0].id : null
  ])
}
