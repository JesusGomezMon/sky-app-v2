# Guía de Despliegue AWS EC2 - SKY App v2.0

## Requisitos
- Cuenta AWS gratuita (Free Tier)
- Par de claves SSH (.pem)

## Paso 1: Crear instancia EC2

1. Ir a **AWS Console → EC2 → Launch Instance**
2. Configuración:
   - **Nombre:** sky-app-server
   - **AMI:** Amazon Linux 2
   - **Tipo:** t2.micro (Free Tier)
   - **Almacenamiento:** 8 GiB gp2 (General Purpose SSD)
   - **Security Group:** Permitir puertos **22** (SSH) y **80** (HTTP)
3. Crear o seleccionar un **Key Pair** (.pem)
4. Lanzar la instancia

## Paso 2: Configurar IAM

Ejecuta `deploy/setup-iam.sh` o crea manualmente en **IAM → Users**:

| Usuario | Grupo | Rol DevOps | Acceso |
|---------|-------|------------|--------|
| dev1-sky | sky-desarrolladores | Desarrollador 1 | EC2 + SSH |
| dev2-sky | sky-desarrolladores | Desarrollador 2 | EC2 + SSH |
| it1-sky | sky-it | IT 1 | EC2 admin + CloudWatch |
| it2-sky | sky-it | IT 2 | Seguridad + S3 backups |
| atencion1-sky | sky-atencion | Atención 1 | Solo consulta |
| atencion2-sky | sky-atencion | Atención 2 | Solo consulta |

## Paso 3: Desplegar la aplicación

```bash
# Conectar por SSH
ssh -i tu-clave.pem ec2-user@<IP-PUBLICA-EC2>

# Clonar repositorio (usa TU cuenta de GitHub, no como colaborador externo)
git clone https://github.com/TU-USUARIO/sky-app-v2.git
cd sky-app-v2

# Ejecutar despliegue
chmod +x deploy/deploy.sh
sudo bash deploy/deploy.sh
```

## Paso 4: Verificar acceso desde cualquier lugar

Abre en el navegador: `http://<IP-PUBLICA-EC2>/api/monitoreo/health`

Deberías ver: `{"status": "ok", "servicio": "SKY App v2.0"}`

## Paso 5: Configurar GitHub Secrets (CD automático)

En GitHub → Settings → Secrets:
- `EC2_HOST`: IP pública de la instancia
- `EC2_USER`: ec2-user
- `EC2_SSH_KEY`: contenido del archivo .pem

## Costo estimado (Free Tier)
- t2.micro: 750 hrs/mes gratis (12 meses)
- 8 GiB EBS: 30 GB gratis
- **Total:** ~$0/mes en Free Tier
