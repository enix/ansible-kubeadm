variable "worker_count" {
  default = 1
}

variable "control_plane_count" {
  default = 2
}

variable "image_name" {
  default = "Ubuntu 20.04 20200611"
}

variable "floating_pool" {
  default = "Public Floating"
}

variable "network_name" {
  default = "internal"
}

variable "ssh_key_path" {
  default = "~/.ssh/id_rsa.pub"
}

variable "stem" {
  default = "kubeadm"
}

variable "allocate_private_net" {
  default = true
}

variable "private_subnet" {
  default = "192.168.199.0/24"
}
