#!/bin/bash
# Script de despliegue en Amazon Linux 2 (EC2 t2.micro)
set -e

APP_DIR="/opt/sky-app"
SERVICE_NAME="sky-app"

echo "=== Despliegue SKY App v2.0 en EC2 ==="

# Actualizar sistema e instalar dependencias
sudo yum update -y
sudo yum install -y python3 python3-pip git

# Crear directorio de la aplicación
sudo mkdir -p $APP_DIR
sudo cp -r sky_app requirements.txt $APP_DIR/
cd $APP_DIR

sudo pip3 install -r requirements.txt

# Crear directorios de datos
sudo mkdir -p $APP_DIR/sky_app/clientes $APP_DIR/sky_app/backups
sudo chown -R ec2-user:ec2-user $APP_DIR

# Configurar servicio systemd para inicio automático
sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null <<EOF
[Unit]
Description=SKY App v2.0 - Gestión de Clientes
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=$APP_DIR
Environment=PORT=80
ExecStart=/usr/bin/python3 $APP_DIR/sky_app/app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo "=== Despliegue completado ==="
echo "Verificar: curl http://localhost/api/monitoreo/health"
sudo systemctl status $SERVICE_NAME --no-pager
