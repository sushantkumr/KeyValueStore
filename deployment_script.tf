provider "aws" {
  region = "us-east-1"
}

terraform {
  required_version = ">= 0.12.6"
}

resource "aws_default_vpc" "default" {
}

locals {
    account_id = data.aws_caller_identity.current.account_id
}

data "aws_subnet_ids" "all" {
  vpc_id = resource.aws_default_vpc.default.id
}

### ECR

resource "aws_ecr_repository" "key-value-store" {
  name                 = "key-value-store"
  image_tag_mutability = "MUTABLE"

  tags = {
    project = "key-value-store"
  }
}

module "ecr_docker_build" {
  source = "github.com/onnimonni/terraform-ecr-docker-build-module"
  dockerfile_folder = "./"
  docker_image_tag = "latest"
  aws_region = "us-east-1"
  ecr_repository_url = "${aws_ecr_repository.key-value-store.repository_url}"
}

### EC2

module "dev_ssh_sg" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "ec2_sg"
  description = "Security group for ec2_sg"
  vpc_id      = resource.aws_default_vpc.default.id

  ingress_cidr_blocks = ["18.206.107.24/29"]
  ingress_rules       = ["ssh-tcp"]
}

module "ec2_sg" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "ec2_sg"
  description = "Security group for ec2_sg"
  vpc_id      = resource.aws_default_vpc.default.id

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["http-80-tcp", "https-443-tcp", "all-icmp"]
  egress_rules        = ["all-all"]
}

data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-ebs"]
  }
}

resource "aws_iam_role" "ec2_role_key_value_store" {
  name = "ec2_role_key_value_store"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

  tags = {
    project = "key-value-store"
  }
}

resource "aws_iam_instance_profile" "ec2_profile_key_value_store" {
  name = "ec2_profile_key_value_store"
  role = aws_iam_role.ec2_role_key_value_store.name
}

resource "aws_iam_role_policy" "ec2_policy" {
  name = "ec2_policy"
  role = aws_iam_role.ec2_role_key_value_store.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_instance" "key_value_store_instance" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.micro"

  root_block_device {
    volume_size = 8
  }

  user_data = <<-EOF
    #!/bin/bash
    set -ex
    sudo yum update -y
    sudo amazon-linux-extras install docker -y
    sudo service docker start
    sudo usermod -a -G docker ec2-user
    sudo curl -L https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    docker login -u AWS -p $(aws ecr get-login-password --region us-east-1) ${local.account_id}.dkr.ecr.us-east-1.amazonaws.com
    docker pull ${module.ecr_docker_build.ecr_image_url}
    docker run -p 5000:5000 ${module.ecr_docker_build.ecr_image_url}

  EOF

  vpc_security_group_ids = [
    module.ec2_sg.security_group_id,
    module.dev_ssh_sg.security_group_id
  ]
  iam_instance_profile = aws_iam_instance_profile.ec2_profile_key_value_store.name

  tags = {
    project = "key-value-store"
  }

  monitoring              = true
  disable_api_termination = false
  ebs_optimized           = true

  depends_on = [
    module.ecr_docker_build,
  ]
}
