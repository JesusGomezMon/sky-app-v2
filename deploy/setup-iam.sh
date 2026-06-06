#!/bin/bash
# Configuración de usuarios IAM para el equipo SKY
# Ejecutar con AWS CLI configurado: bash deploy/setup-iam.sh

echo "=== Configuración IAM - Equipo SKY ==="
echo ""
echo "Este script genera las políticas IAM. Ejecuta los comandos manualmente en AWS CLI"
echo "o usa la consola de AWS IAM."
echo ""

cat << 'POLICY_DEV'
# --- POLÍTICA DESARROLLADORES (acceso completo a EC2 y despliegue) ---
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:StartInstances",
        "ec2:StopInstances",
        "ec2:RebootInstances",
        "ssm:StartSession"
      ],
      "Resource": "*"
    }
  ]
}
POLICY_DEV

cat << 'POLICY_IT'
# --- POLÍTICA IT (administración, respaldos, monitoreo) ---
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "*"
    }
  ]
}
POLICY_IT

cat << 'POLICY_ATENCION'
# --- POLÍTICA ATENCIÓN AL CLIENTE (solo lectura/consulta) ---
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances"
      ],
      "Resource": "*"
    }
  ]
}
POLICY_ATENCION

echo ""
echo "=== USUARIOS A CREAR EN IAM ==="
echo ""
echo "Grupo: sky-desarrolladores"
echo "  - dev1-sky (Desarrollador 1) - Política: AmazonEC2ReadOnlyAccess + custom deploy"
echo "  - dev2-sky (Desarrollador 2) - Política: AmazonEC2ReadOnlyAccess + custom deploy"
echo ""
echo "Grupo: sky-it"
echo "  - it1-sky (IT 1 - Infraestructura) - Política: AmazonEC2FullAccess (limitada)"
echo "  - it2-sky (IT 2 - Seguridad) - Política: CloudWatchReadOnlyAccess + S3 backup"
echo ""
echo "Grupo: sky-atencion"
echo "  - atencion1-sky (Atención 1) - Política: solo DescribeInstances"
echo "  - atencion2-sky (Atención 2) - Política: solo DescribeInstances"
echo ""
echo "=== COMANDOS AWS CLI (ejemplo) ==="
echo ""
echo "# Crear grupos"
echo "aws iam create-group --group-name sky-desarrolladores"
echo "aws iam create-group --group-name sky-it"
echo "aws iam create-group --group-name sky-atencion"
echo ""
echo "# Crear usuario y agregar a grupo"
echo "aws iam create-user --user-name dev1-sky"
echo "aws iam add-user-to-group --user-name dev1-sky --group-name sky-desarrolladores"
echo ""
echo "# Repetir para: dev2-sky, it1-sky, it2-sky, atencion1-sky, atencion2-sky"
