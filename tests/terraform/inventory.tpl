[kube_control_plane]
%{ for server, ip in kube_control_plane ~}
${server} ansible_host=${ip}
%{ endfor ~}

[kube_workers]
%{ for server, ip in kube_workers ~}
${server} ansible_host=${ip}
%{ endfor ~}

[all:vars]
control_plane_endpoint=127.0.0.1:7443
cluster_config={"networking": {"podSubnet": "10.253.0.0/11"}}
kubelet_config={"cgroupDriver": "systemd"}
ansible_user=ubuntu
ansible_become=true
ansible_ssh_pipelining=True
