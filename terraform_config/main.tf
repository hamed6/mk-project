terraform {
  required_version=">=1.0"
  required_providers {
    aws={
        source="hashicorp/aws"
    }
  }
}

provider "aws" {
    region = "us-east-1"
}

# Network configurations
resource "aws_vpc" "macrack_vpc_01" {
  cidr_block = "10.0.0.0/26"
}

resource "aws_subnet" "macrack_subnet_01" {
  
}

resource "aws_route_table" "macrack_routetable_01" {
  
}

resource "aws_internet_gateway" "macrack_igw_01" {
  
}

# ----------------------------------------------------
# Compute configurations
resource "aws_ami" "macrack_ec2_01" {
  
}

resource "aws_s3_bucket" "macrack_s3_01" {
  
}

resource "aws_rds_cluster" "macrack_rds_01" {
  
}