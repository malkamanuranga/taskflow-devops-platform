terraform {
  required_providers {
    kubernetes = { source = "hashicorp/kubernetes", version = "~> 2.30" }
  }
}

provider "kubernetes" {
  config_path    = pathexpand("~/.kube/config")
  config_context = "kind-devops"
}

resource "kubernetes_namespace" "taskflow" {
  metadata { name = "taskflow" }
} 
} clear()
