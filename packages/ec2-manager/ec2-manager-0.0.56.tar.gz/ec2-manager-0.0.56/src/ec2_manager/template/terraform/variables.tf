# Default AWS Region used to deploy resources
variable "aws_region" {
  type = string
  default = ""
}

variable "type" {
  type = string
  default = ""
}

variable "user_data_file" {
  default = null
}

variable "ssh_key_name" {
  default = null
}

variable "vpc_name" {
  description = "The name of the existing VPC to deploy the instances into"
  default = "Default VPC"
}

variable "platform" {
  description = "The platform of the ami i.e. amzn2, ubuntu"
  default = "amzn2"
}

variable "architecture" {
  description = "The cpu architecture"
  default = "arm64"
}

variable "private_subnet_cidr" {
  type = string
  default = ""
}

variable "public_subnet_cidr" {
  default = ""
}

variable "instances" {
  type = string
  description = "A base64 encoded json string of instance names and their attributes"
  default = ""
}

variable "volume_size" {
  default = 8
}

locals {
  to_cidr_range = var.private_subnet_cidr == "" ? "0.0.0.0/0" : var.public_subnet_cidr
  subnet_cidr_range = var.private_subnet_cidr == "" ? var.public_subnet_cidr : var.private_subnet_cidr
  instances = var.instances == "" ? {} : jsondecode(base64decode(var.instances))
}