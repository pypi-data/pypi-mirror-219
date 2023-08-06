variable "cluster_name" {
  type    = string
  default = {{ cluster_name }}
}

variable "state_region" {
  type    = string
  default = {{ state_region }}
}

variable "bucket_name" {
  type    = string
  default = {{ bucket_name }}
}

variable "dynamodb_table" {
  type    = string
  default = {{ dynamodb_table }}
}

# cluster_name = "demo"