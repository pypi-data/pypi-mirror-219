#!/bin/bash

%{ for key, value in envs }
export ${key}=${value}
%{ endfor ~}

# install packages
sudo apt update -y && sudo apt install unzip git software-properties-common acl -y

# install aws cli
sudo curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo unzip awscliv2.zip
sudo rm awscliv2.zip
sudo ./aws/install

# install ssm agent
sudo snap install amazon-ssm-agent --classic
sudo snap start amazon-ssm-agent

# install docker
sudo apt-get update -y
sudo apt-get install ca-certificates curl gnupg lsb-release -y
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo apt-get update -y --allow-unauthenticated
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo setfacl -R -m u:ubuntu:rwx /var/run/docker.sock
sudo setfacl -R -m u:ssm-user:rwx /var/run/docker.sock

# this is a work around for a bug with the terraform spot instance resource
# https://github.com/hashicorp/terraform/issues/3263
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
SPOT_REQ_ID=$(aws --region $AWS_REGION ec2 describe-instances --instance-ids "$INSTANCE_ID"  --query 'Reservations[0].Instances[0].SpotInstanceRequestId' --output text)
TAGS=$(aws --region $AWS_REGION ec2 describe-spot-instance-requests --spot-instance-request-ids "$SPOT_REQ_ID" --query 'SpotInstanceRequests[0].Tags')
aws --region $AWS_REGION ec2 create-tags --resources "$INSTANCE_ID" --tags "$TAGS"

%{ for key, value in envs }
unset ${key}
%{ endfor ~}