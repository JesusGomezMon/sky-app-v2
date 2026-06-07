# Guia AWS desde cero - SKY App v2.0

Guia completa para crear una instancia EC2 nueva e instalar la aplicacion.

---

## PARTE 1: Borrar la instancia vieja (opcional)

1. Entra a [AWS Console EC2](https://console.aws.amazon.com/ec2/)
2. Region: **us-east-2** (Ohio) — o la que prefieras
3. **Instancias** → selecciona la instancia vieja (`sky-app-v2` o `i-095a2a735d92b3ce8`)
4. **Instancia → Terminar (eliminar) instancia** → Confirmar

> Esto evita confusiones y costos extra.

---

## PARTE 2: Crear instancia nueva

### Paso 1 — Launch Instance

1. EC2 → **Launch instance**
2. Configura asi:

| Campo | Valor |
|-------|-------|
| **Name** | `sky-app-v2` |
| **AMI** | Amazon Linux 2023 (Free tier eligible) |
| **Instance type** | `t2.micro` |
| **Key pair** | Create new → nombre: `sky-key` → **Download .pem** (guardalo!) |
| **Storage** | 8 GiB gp3 |

### Paso 2 — Security Group (MUY IMPORTANTE)

En **Network settings** → **Edit** → crea reglas:

| Type | Port | Source |
|------|------|--------|
| SSH | 22 | 0.0.0.0/0 |
| HTTP | 80 | 0.0.0.0/0 |

> Sin HTTP puerto 80 la app no se ve desde internet.

### Paso 3 — User Data (instalacion automatica)

1. Desplazate a **Advanced details**
2. En **User data** pega el contenido del archivo `deploy/user-data.sh` del repo
3. O pega esto directamente:

```bash
#!/bin/bash
exec > /var/log/sky-app-boot.log 2>&1
dnf install -y git python3 python3-pip
cd /home/ec2-user
git clone https://github.com/JesusGomezMon/sky-app-v2.git
cd sky-app-v2
bash deploy/install.sh
```

### Paso 4 — Launch

1. Clic **Launch instance**
2. Espera 2-3 minutos hasta que **Instance state** = **Running**
3. Copia la **IP publica** (ej: `3.128.xxx.xxx`)

---

## PARTE 3: Verificar que funciona

### Opcion A — Desde tu navegador (cualquier lugar)

Abre:
```
http://TU-IP-PUBLICA/api/monitoreo/health
```

Debes ver:
```json
{"servicio":"SKY App v2.0","status":"ok"}
```

### Opcion B — Si User Data no funciono (manual)

1. EC2 → tu instancia → **Connect**
2. Pestaña **EC2 Instance Connect** → **Connect**
3. Debe decir `[ec2-user@ip-...]$` (NO cloudshell-user)
4. Pega:

```bash
curl -sO https://raw.githubusercontent.com/JesusGomezMon/sky-app-v2/main/deploy/install.sh && bash install.sh
```

---

## PARTE 4: Probar la aplicacion

```bash
# Crear cliente
curl -X POST http://TU-IP/api/clientes \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan Perez","direccion":"Av Reforma 123","telefono":"5551234567","correo":"juan@email.com"}'

# Listar clientes
curl http://TU-IP/api/clientes

# Health check
curl http://TU-IP/api/monitoreo/health
```

---

## PARTE 5: IAM - Usuarios del equipo (requerido por la tarea)

AWS Console → **IAM** → **User groups** → Create group:

| Grupo | Usuarios | Politica sugerida |
|-------|----------|-------------------|
| sky-desarrolladores | dev1-sky, dev2-sky | AmazonEC2ReadOnlyAccess |
| sky-it | it1-sky, it2-sky | AmazonEC2ReadOnlyAccess + CloudWatchReadOnlyAccess |
| sky-atencion | atencion1-sky, atencion2-sky | AmazonEC2ReadOnlyAccess |

Para cada usuario: IAM → Users → Create user → Add to group.

---

## PARTE 6: Si algo falla

### Ver logs de instalacion automatica
```bash
# En EC2 Instance Connect
sudo cat /var/log/sky-app-boot.log
```

### Ver estado del servicio
```bash
sudo systemctl status sky-app
sudo journalctl -u sky-app -n 30 --no-pager
```

### Reiniciar la app
```bash
sudo systemctl restart sky-app
curl http://localhost/api/monitoreo/health
```

---

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Timeout en navegador | Puerto 80 cerrado | Abrir HTTP en Security Group |
| `login:` en terminal | Consola serial, no Instance Connect | EC2 → Connect → EC2 Instance Connect |
| `/home/ec2-user not found` | Estas en Cloud Shell | Usar Instance Connect |
| `pip externally-managed` | Amazon Linux 2023 | El script `install.sh` usa venv (ya corregido) |

---

## Checklist final

- [ ] Instancia t2.micro Amazon Linux 2023 corriendo
- [ ] Security Group con puertos 22 y 80 abiertos
- [ ] `http://IP/api/monitoreo/health` responde OK
- [ ] Puedes crear y listar clientes via API
- [ ] 6 usuarios IAM creados en 3 grupos
- [ ] Repositorio GitHub con Actions funcionando

---

## Costo

Free Tier (12 meses): **~$0/mes** (750 h t2.micro + 30 GB EBS)
