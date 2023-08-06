provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket         = var.bucket_name
    key            = "global/s3/terraform.tfstate"
    region         = var.state_region
    dynamodb_table = var.dynamodb_table
    encrypt        = true
  }
}

# state-bucket-name = "terraform-state-bucket-devopipe"
# state-region = "us-east-1"

#resource "aws_s3_bucket" "terraform_state" {
#  bucket = "terraform-state-bucket-devopipe"
#
#  lifecycle {
#    prevent_destroy = true
#  }
#
#  versioning {
#    enabled = true
#  }
#
#  server_side_encryption_configuration {
#    rule {
#      apply_server_side_encryption_by_default {
#        sse_algorithm = "AES256"
#      }
#    }
#  }
#}
#
#
#resource "aws_dynamodb_table" "terraform_locks" {
#  name         = "terraform-state-locking"
#  billing_mode = "PAY_PER_REQUEST"
#  hash_key     = "LockID"
#
#  attribute {
#    name = "LockID"
#    type = "S"
#  }
#}
#

#
#
#resource "aws_ecr_repository" "devolink_front" {
#  name                 = "devolink_front"
#  image_tag_mutability = "MUTABLE"
#
#  image_scanning_configuration {
#    scan_on_push = false
#  }
#
#  lifecycle {
#    prevent_destroy = true
#  }
#}
#
#resource "aws_ecr_repository" "devopipe_back" {
#  name                 = "devolink_back"
#  image_tag_mutability = "MUTABLE"
#
#  image_scanning_configuration {
#    scan_on_push = false
#  }
#
#  lifecycle {
#    prevent_destroy = true
#  }
#}
#
#resource "aws_ecr_repository" "devopipe_dbmigrations" {
#  name                 = "devolink_dbmigrations"
#  image_tag_mutability = "MUTABLE"
#
#  image_scanning_configuration {
#    scan_on_push = false
#  }
#
#  lifecycle {
#    prevent_destroy = true
#  }
#}


