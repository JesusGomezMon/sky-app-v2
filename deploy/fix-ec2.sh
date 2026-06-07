#!/bin/bash
# Reparar SKY App en EC2 - pegar en Instance Connect
set -e

APP_DIR="/opt/sky-app"
SERVICE_NAME="sky-app"
SRC_DIR="$HOME/sky-app-v2"

echo "=== Reparando SKY App ==="

# Ir al codigo
if [ -d "$SRC_DIR" ]; then
    cd "$SRC_DIR"
elif [ -d "$APP_DIR" ]; then
    cd "$APP_DIR/.."
else
    echo "ERROR: Ejecuta primero: git clone https://github.com/JesusGomezMon/sky-app-v2.git"
    exit 1
fi

# Instalar dependencias
if command -v dnf &>/dev/null; then
    sudo dnf install -y python3 python3-pip
else
    sudo yum install -y python3 python3-pip
fi

sudo mkdir -p $APP_DIR
sudo cp -r sky_app requirements.txt $APP_DIR/
cd $APP_DIR
sudo pip3 install -r requirements.txt
sudo mkdir -p $APP_DIR/sky_app/clientes $APP_DIR/sky_app/backups

PYTHON_BIN=$(readlink -f $(which python3))

# Servicio como root para usar puerto 80 sin problemas
sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null <<EOF
[Unit]
Description=SKY App v2.0
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR
Environment=PORT=80
Environment=PYTHONPATH=$APP_DIR
ExecStart=$PYTHON_BIN $APP_DIR/sky_app/app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

sleep 3
echo ""
echo "=== Estado del servicio ==="
sudo systemctl status $SERVICE_NAME --no-pager || true
echo ""
echo "=== Prueba local ==="
curl -s http://localhost/api/monitoreo/health && echo "" || echo "FALLO - ver logs abajo"
echo ""
echo "=== Ultimos logs ==="
sudo journalctl -u $SERVICE_NAME -n 20 --no-pager
