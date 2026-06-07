#!/bin/bash
# Instalacion SKY App - Amazon Linux 2023 / EC2 Instance Connect
# Ejecutar como ec2-user: bash ec2-install.sh
set -ex

echo "=== Usuario: $(whoami) | Host: $(hostname) ==="

# Solo en EC2, no Cloud Shell
if [[ "$(whoami)" == "cloudshell-user" ]]; then
  echo "ERROR: Estas en Cloud Shell. Ve a EC2 -> Connect -> EC2 Instance Connect"
  exit 1
fi

cd /home/ec2-user
rm -rf sky-app-v2
git clone https://github.com/JesusGomezMon/sky-app-v2.git
cd sky-app-v2

sudo dnf install -y python3 python3-pip git

# Copiar a /opt
sudo rm -rf /opt/sky-app
sudo mkdir -p /opt/sky-app
sudo cp -r sky_app requirements.txt /opt/sky-app/
cd /opt/sky-app

# Venv evita error "externally-managed-environment" en AL2023
sudo python3 -m venv /opt/sky-app/venv
sudo /opt/sky-app/venv/bin/pip install --upgrade pip
sudo /opt/sky-app/venv/bin/pip install flask
sudo mkdir -p /opt/sky-app/sky_app/clientes /opt/sky-app/sky_app/backups

# Servicio systemd puerto 80
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
echo "=== PRUEBA LOCAL ==="
curl -v http://localhost/api/monitoreo/health || true
echo ""
echo "=== ESTADO SERVICIO ==="
sudo systemctl status sky-app --no-pager || true
echo ""
echo "=== LOGS SI FALLA ==="
sudo journalctl -u sky-app -n 30 --no-pager || true
