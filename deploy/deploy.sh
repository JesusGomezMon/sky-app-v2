#!/bin/bash
# Script de despliegue en Amazon Linux 2 / 2023 (EC2 t2.micro)
set -e

APP_DIR="/opt/sky-app"
SERVICE_NAME="sky-app"

echo "=== Despliegue SKY App v2.0 en EC2 ==="

# Detectar gestor de paquetes
if command -v dnf &>/dev/null; then
    PKG="dnf"
else
    PKG="yum"
fi

sudo $PKG update -y
sudo $PKG install -y python3 python3-pip git

# Crear directorio de la aplicacion
sudo mkdir -p $APP_DIR
sudo cp -r sky_app requirements.txt $APP_DIR/
cd $APP_DIR

sudo pip3 install -r requirements.txt

# Permitir que Python use el puerto 80 sin root
PYTHON_BIN=$(readlink -f $(which python3))
sudo setcap CAP_NET_BIND_SERVICE=+eip "$PYTHON_BIN" 2>/dev/null || true

# Crear directorios de datos
sudo mkdir -p $APP_DIR/sky_app/clientes $APP_DIR/sky_app/backups
sudo chown -R ec2-user:ec2-user $APP_DIR

# Configurar servicio systemd para inicio automatico
sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null <<EOF
[Unit]
Description=SKY App v2.0 - Gestion de Clientes
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR
Environment=PORT=80
Environment=PYTHONPATH=$APP_DIR
ExecStart=$PYTHON_BIN $APP_DIR/sky_app/app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo ""
echo "=== Despliegue completado ==="
sleep 2
curl -s http://localhost/api/monitoreo/health || echo "(Esperando arranque...)"
echo ""
sudo systemctl status $SERVICE_NAME --no-pager
echo ""
echo "Abre en tu navegador: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo 'TU-IP')/api/monitoreo/health"
