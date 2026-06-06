# SKY App v2.0 - Gestión de Clientes

Aplicación Python con arquitectura DDD, microservicios y DevOps para la empresa SKY.

## Estructura del Proyecto

```
sky_app/
├── clientes/              # Datos JSON de clientes
├── backups/               # Respaldos automáticos
├── dominio/               # DDD: entidades y value objects
├── infraestructura/       # Repositorio JSON
├── microservicios/
│   ├── gestion_clientes.py
│   ├── gestion_servicios.py
│   ├── consultas.py
│   ├── respaldos.py
│   └── monitoreo.py
├── pruebas/
└── app.py                 # API REST Flask
```

## Instalación Local

```bash
pip install -r requirements.txt
python sky_app/app.py
```

La API estará en `http://localhost:5000`

## Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/clientes` | Listar clientes |
| POST | `/api/clientes` | Crear cliente |
| GET | `/api/clientes/{id}` | Buscar cliente |
| PUT | `/api/clientes/{id}` | Actualizar cliente |
| DELETE | `/api/clientes/{id}` | Eliminar cliente |
| POST | `/api/servicios` | Agregar servicio |
| GET | `/api/consultas/{id}` | Consultar información |
| POST | `/api/respaldos` | Generar respaldo |
| GET | `/api/monitoreo/health` | Estado del sistema |

## Pruebas

```bash
pytest sky_app/pruebas/ -v
```

## GitHub Actions (DevOps)

| Workflow | Trigger | Función |
|----------|---------|---------|
| `ci-pruebas.yml` | Push/PR | Pruebas automáticas |
| `nuevo-cliente.yml` | Manual / Issue | Registrar cliente |
| `modificar-cliente.yml` | Manual / Issue | Modificar cliente |
| `consulta-cliente.yml` | Manual / Issue | Consultar cliente |
| `solicitud-mejora.yml` | Issue label `mejora` | Procesar mejoras |
| `modificacion-codigo.yml` | Push develop/PR | Validar código |
| `nueva-funcion.yml` | Issue label `nueva-funcion` | Nueva funcionalidad |
| `cd-aws-deploy.yml` | Push main | Despliegue AWS |

## Equipo DevOps y Roles GitHub

| Miembro | Rol GitHub | Responsabilidad |
|---------|------------|-----------------|
| Desarrollador 1 | Admin | Backend, APIs |
| Desarrollador 2 | Admin | Pruebas, CI |
| IT 1 | Maintain | Infraestructura AWS |
| IT 2 | Maintain | Seguridad, respaldos |
| Atención 1 | Triage | Issues, consultas |
| Atención 2 | Triage | Reportes, validación |

## Despliegue AWS EC2

Ver [docs/AWS-DEPLOY.md](docs/AWS-DEPLOY.md) para instrucciones completas.

```bash
ssh -i clave.pem ec2-user@<IP-EC2>
git clone https://github.com/TU-USUARIO/sky-app-v2.git
cd sky-app-v2 && sudo bash deploy/deploy.sh
```

## Subir a GitHub (tu cuenta)

```bash
git init
git add .
git commit -m "feat: SKY App v2.0 - implementación completa"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/sky-app-v2.git
git push -u origin main
```

## Guía para Video

Ver [docs/GUIA-VIDEO.md](docs/GUIA-VIDEO.md)
