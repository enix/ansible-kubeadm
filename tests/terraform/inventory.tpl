[kube_control_plane]
%{ for server, ip in kube_control_plane ~}
${server} ansible_host=${ip}
%{ endfor ~}

[kube_nodes]
%{ for server, ip in kube_nodes ~}
${server} ansible_host=${ip}
%{ endfor ~}

[all:vars]
control_plane_endpoint=127.0.0.1:7443
ansible_user=ubuntu
ansible_become=true
ansible_ssh_pipelining=True
