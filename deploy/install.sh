#!/bin/bash
# SKY App v2.0 - Instalacion en EC2 (Amazon Linux 2023)
# Ejecutar SOLO en EC2 Instance Connect como ec2-user
set -e

if [[ "$(whoami)" == "cloudshell-user" ]]; then
  echo "ERROR: Estas en Cloud Shell. Usa EC2 -> Connect -> EC2 Instance Connect"
  exit 1
fi

echo "=== Instalando SKY App v2.0 ==="

sudo dnf install -y git python3 python3-pip

cd /home/ec2-user
sudo rm -rf sky-app-v2
git clone https://github.com/JesusGomezMon/sky-app-v2.git
cd sky-app-v2
sudo chown -R ec2-user:ec2-user /home/ec2-user/sky-app-v2

sudo rm -rf /opt/sky-app
sudo mkdir -p /opt/sky-app
sudo cp -r sky_app requirements.txt /opt/sky-app/
cd /opt/sky-app

sudo python3 -m venv /opt/sky-app/venv
sudo /opt/sky-app/venv/bin/pip install --upgrade pip
sudo /opt/sky-app/venv/bin/pip install flask
sudo mkdir -p /opt/sky-app/sky_app/clientes /opt/sky-app/sky_app/backups

sudo tee /etc/systemd/system/sky-app.service > /dev/null << 'EOF'
[Unit]
Description=SKY App v2.0
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/sky-app
Environment=PORT=80
Environment=PYTHONPATH=/opt/sky-app
ExecStart=/opt/sky-app/venv/bin/python /opt/sky-app/sky_app/app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable sky-app
sudo systemctl restart sky-app
sleep 5

echo ""
echo "=== RESULTADO ==="
curl -s http://localhost/api/monitoreo/health && echo ""
echo ""
echo "Abre en tu navegador: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)/api/monitoreo/health"
