locals {
  ssh_key_glob = tolist(fileset("/", pathexpand(var.ssh_key_path)))
  ssh_key_path = "/${length(local.ssh_key_glob) >= 1 ? element(local.ssh_key_glob, 0) : pathexpand(var.ssh_key_path)}"
}

data "local_file" "ssh_key" {
  filename = local.ssh_key_path
}

resource "openstack_compute_keypair_v2" "ssh_deploy" {
  name       = var.stem
  public_key = data.local_file.ssh_key.content
}
