#!/bin/bash
# Reparar instalacion completa en EC2
set -e
echo "=== Reparando SKY App ==="

sudo dnf install -y git python3 python3-pip

cd /home/ec2-user
sudo rm -rf sky-app-v2
git clone https://github.com/JesusGomezMon/sky-app-v2.git

sudo rm -rf /opt/sky-app
sudo mkdir -p /opt/sky-app
sudo cp -r /home/ec2-user/sky-app-v2/sky_app /home/ec2-user/sky-app-v2/requirements.txt /opt/sky-app/

cd /opt/sky-app
sudo python3 -m venv venv
sudo ./venv/bin/pip install --upgrade pip
sudo ./venv/bin/pip install flask
sudo mkdir -p sky_app/clientes sky_app/backups

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
ExecStart=/opt/sky-app/venv/bin/python3 /opt/sky-app/sky_app/app.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable sky-app
sudo systemctl restart sky-app

echo ""
echo "=== Verificacion ==="
ls -la /opt/sky-app/venv/bin/python3
ls -la /opt/sky-app/sky_app/menu.py
curl -s http://localhost/api/monitoreo/health
echo ""
echo "=== Para abrir el menu ==="
echo "sudo /opt/sky-app/venv/bin/python3 /opt/sky-app/sky_app/menu.py"
