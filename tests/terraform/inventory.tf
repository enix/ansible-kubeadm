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
  })
  filename = "${var.stem}-hosts.cfg"
}


output "inventory" {
  value = local_file.inventory.filename
}
