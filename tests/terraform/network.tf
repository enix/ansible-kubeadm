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
