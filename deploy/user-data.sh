#!/bin/bash
# User Data - Pegar al crear la instancia EC2
exec > /var/log/sky-app-boot.log 2>&1
set -x

dnf install -y git python3 python3-pip

# Ejecutar instalacion como ec2-user
sudo -u ec2-user bash << 'SCRIPT'
cd /home/ec2-user
git clone https://github.com/JesusGomezMon/sky-app-v2.git
cd sky-app-v2
bash deploy/install.sh
SCRIPT
