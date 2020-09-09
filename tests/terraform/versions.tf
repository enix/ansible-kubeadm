terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
    }
    openstack = {
      source = "terraform-providers/openstack"
    }
  }
  required_version = ">= 0.13"
}
