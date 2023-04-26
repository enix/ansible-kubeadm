locals {
  image_match_user = [
    ["U|ubuntu.*", "ubuntu"],
    ["D|debian.*", "debian"]
  ]
  login_user = element([for match in local.image_match_user: match[1] if length(regexall(match[0], var.image_name)) > 0], 1)
}

resource "local_file" "inventory" {
  content = templatefile("${path.module}/inventory.tpl", {
    kube_control_plane = zipmap(
      openstack_compute_instance_v2.control_plane.*.name,
      openstack_networking_floatingip_v2.floatip_cp.*.address
    ),
    kube_workers = zipmap(
      openstack_compute_instance_v2.workers.*.name,
      openstack_networking_floatingip_v2.floatip_workers.*.address
    )
    allocate_private_net = var.allocate_private_net
    private_subnet       = var.private_subnet
    login_user           = local.login_user
  })
  filename = "${var.inventory_dir}/${var.stem}-hosts.cfg"
}


output "inventory" {
  value = local_file.inventory.filename
}
