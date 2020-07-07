variable "node_count" {
  default = 1
}

variable "control_plane_count" {
  default = 2
}

variable "image_name"{
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
