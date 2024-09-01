terraform {
  backend "remote" {
    organization = "beaver"
    workspaces {
      name = "beaver-api"
    }
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}