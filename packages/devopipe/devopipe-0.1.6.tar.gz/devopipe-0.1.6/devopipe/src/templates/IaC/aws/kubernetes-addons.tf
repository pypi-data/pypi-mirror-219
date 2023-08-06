module "kubernetes_addons" {
  source = "github.com/aws-ia/terraform-aws-eks-blueprints//modules/kubernetes-addons?ref=v4.25.0"

  eks_cluster_id = module.eks_blueprints.eks_cluster_id

  # EKS Add-ons
  enable_amazon_eks_aws_ebs_csi_driver = true

  enable_aws_load_balancer_controller = true

  enable_metrics_server = true
  enable_cert_manager   = true

  enable_cluster_autoscaler = true


  depends_on = [module.eks_blueprints]
}

provider "helm" {
  kubernetes {
    #alias = "cluster_eks"
    host                   = module.eks_blueprints.eks_cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks_blueprints.eks_cluster_certificate_authority_data)

    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      command     = "aws"
      args        = ["eks", "get-token", "--cluster-name", module.eks_blueprints.eks_cluster_id]
    }
  }

}

{{create_namespace}}
{{create_vcluster}}

# Add create-namespaces.yaml

# Add create-vcluster.yaml


# helm install argocd -n argocd --create-namespace argo/argo-cd --version 3.35.4 -f terraform/values/argocd.yaml
resource "helm_release" "argocd" {
  name = "argocd"

  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  namespace        = "argocd"
  create_namespace = true
  version          = "3.35.4"

  values     = [file("values/argocd.yaml")]
  depends_on = [module.eks_blueprints]
}



# Add Prometheus Helm repository
resource "null_resource" "prometheus_repository" {
  provisioner "local-exec" {
    command = "helm repo add prometheus-community https://prometheus-community.github.io/helm-charts"
  }
}

# Add Loki Helm repository
resource "null_resource" "loki_repository" {
  provisioner "local-exec" {
    command = "helm repo add grafana https://grafana.github.io/helm-charts"
  }
}

# Install Prometheus
resource "null_resource" "prometheus_installation" {
  depends_on = [null_resource.prometheus_repository]

  provisioner "local-exec" {
    command = "helm upgrade --install prometheus prometheus-community/kube-prometheus-stack --namespace monitor --create-namespace"
  }
}

# Install Loki
resource "null_resource" "loki_installation" {
  depends_on = [null_resource.loki_repository]

  provisioner "local-exec" {
    command = "helm install  loki grafana/loki --namespace=monitoring --create-namespace"
  }
}
