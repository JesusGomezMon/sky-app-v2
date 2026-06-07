#!/bin/bash
# SKY App - Instalacion completa en un solo comando
# Copiar TODO y pegar en EC2 Instance Connect
set -e
export HOME=/home/ec2-user
cd /home/ec2-user
command -v git >/dev/null || sudo yum install -y git || sudo dnf install -y git
[ -d sky-app-v2 ] || git clone https://github.com/JesusGomezMon/sky-app-v2.git
cd sky-app-v2
sudo yum install -y python3 python3-pip 2>/dev/null || sudo dnf install -y python3 python3-pip
sudo mkdir -p /opt/sky-app/sky_app/clientes /opt/sky-app/sky_app/backups
sudo cp -r /home/ec2-user/sky-app-v2/sky_app /home/ec2-user/sky-app-v2/requirements.txt /opt/sky-app/
cd /opt/sky-app && sudo pip3 install -r requirements.txt
PY=$(readlink -f $(which python3))
sudo bash -c "cat > /etc/systemd/system/sky-app.service" << EOF
[Unit]
Description=SKY App v2.0
After=network.target
[Service]
Type=simple
User=root
WorkingDirectory=/opt/sky-app
Environment=PORT=80
Environment=PYTHONPATH=/opt/sky-app
ExecStart=$PY /opt/sky-app/sky_app/app.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload && sudo systemctl enable sky-app && sudo systemctl restart sky-app
sleep 4
echo "=== RESULTADO ==="
curl -s http://localhost/api/monitoreo/health || sudo journalctl -u sky-app -n 15 --no-pager
