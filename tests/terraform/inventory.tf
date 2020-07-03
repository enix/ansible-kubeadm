resource "local_file" "inventory" {
  content   = templatefile("${path.module}/inventory.tpl",{
    kube_control_plane = zipmap(
        openstack_compute_instance_v2.control_plane.*.name,
        openstack_networking_floatingip_v2.floatip_cp.*.address
    ),
    kube_nodes = zipmap(
        openstack_compute_instance_v2.nodes.*.name,
        openstack_networking_floatingip_v2.floatip_nodes.*.address
    )
  })
  filename  = "${var.stem}-hosts.cfg"
}


output "inventory" {
  value = local_file.inventory.filename
}
