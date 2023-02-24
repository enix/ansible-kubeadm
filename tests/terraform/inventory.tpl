[kube_control_plane]
%{ for server, ip in kube_control_plane ~}
${server} ansible_host=${ip}
%{ endfor ~}

[kube_workers]
%{ for server, ip in kube_workers ~}
${server} ansible_host=${ip}
%{ endfor ~}

[all:vars]
%{ if allocate_private_net == true ~}
kube_control_plane_cidr="${private_subnet}"
kubelet_node_ip_cidr="${private_subnet}"
%{ endif ~}
fix_dns=true
ansible_user=ubuntu
ansible_become=true
ansible_ssh_pipelining=True
