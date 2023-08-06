provider "aws" {
  region = var.region
  #"us-east-1"
}

#terraform {
#  backend "s3" {
#    bucket         = "terraform-state-bucket-devopipe"
#    key            = "global/s3/terraform.tfstate"
#    region         = "us-east-1"
#    dynamodb_table = "terraform-state-locking"
#    encrypt        = true
#  }
#}

resource "aws_s3_bucket" "terraform_state" {
  bucket = var.bucket_name
  #"terraform-state-bucket-devopipe"

  lifecycle {
    prevent_destroy = true
  }

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}


resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locking"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}



resource "aws_ecr_repository" "frontend" {
  name                 = var.project_name + "_front"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_ecr_repository" "backend" {
  name                 = var.project_name + "_back"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_ecr_repository" "dbmigrations" {
  name                 = var.project_name + "_dbmigrations"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }

  lifecycle {
    prevent_destroy = true
  }
}
