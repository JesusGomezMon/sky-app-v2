#!/bin/bash
# User Data - Pegar al crear la instancia EC2 (Advanced details -> User data)
# Instala SKY App automaticamente al encender la instancia
exec > /var/log/sky-app-boot.log 2>&1
set -x

dnf install -y git python3 python3-pip

cd /home/ec2-user
git clone https://github.com/JesusGomezMon/sky-app-v2.git
cd sky-app-v2
bash deploy/install.sh
