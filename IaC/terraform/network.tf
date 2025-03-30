data "aws_availability_zones" "available" { state = "available" }

locals {
  azs_count = length(var.availability_zones)
  azs_names = var.availability_zones
}

resource "aws_vpc" "production-vpc" {
  cidr_block           = "10.10.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags                 = { Name = "vpc" }
}

resource "aws_subnet" "public" {
  count             = local.azs_count
  vpc_id            = aws_vpc.production-vpc.id
  availability_zone = local.azs_names[count.index]
  cidr_block        = cidrsubnet(aws_vpc.production-vpc.cidr_block, 8, 10 + count.index) # 10.10.10.0/24
  tags              = { Name = "public-${local.azs_names[count.index]}" }
}




resource "aws_route_table" "public-route-table" {
  vpc_id = aws_vpc.production-vpc.id
}


resource "aws_route_table_association" "public" {
  count          = local.azs_count
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public-route-table.id
}


resource "aws_internet_gateway" "production-igw" {
  vpc_id = aws_vpc.production-vpc.id
}

resource "aws_route" "public-internet-igw-route" {
  route_table_id         = aws_route_table.public-route-table.id
  gateway_id             = aws_internet_gateway.production-igw.id
  destination_cidr_block = "0.0.0.0/0"
}
