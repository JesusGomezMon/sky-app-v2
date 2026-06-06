# Guía para el Video de Demostración

Usa esta guía como guion para tu video explicando cada indicación.

## 1. GitHub - Proyecto colaborativo (2 min)

- Mostrar repositorio en **tu cuenta** (no como colaborador invitado)
- Settings → Collaborators: mostrar miembros del equipo y roles
- Explicar roles DevOps:
  - **Desarrolladores:** Admin (código, PRs)
  - **IT:** Maintain (infraestructura)
  - **Atención al cliente:** Triage (issues, consultas)

## 2. Aplicación Python (3 min)

- Mostrar estructura `sky_app/` con DDD y microservicios
- Ejecutar localmente: `python sky_app/app.py`
- Demostrar CRUD:
  - **Agregar:** POST `/api/clientes`
  - **Consultar:** GET `/api/clientes/{id}`
  - **Modificar:** PUT `/api/clientes/{id}`
  - **Eliminar:** DELETE `/api/clientes/{id}`

```bash
# Ejemplos con curl
curl -X POST http://localhost:5000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan Pérez","direccion":"Av. Reforma 123","telefono":"5551234567","correo":"juan@email.com"}'

curl http://localhost:5000/api/clientes
curl http://localhost:5000/api/monitoreo/health
```

## 3. GitHub Actions - 6 flujos (4 min)

En Actions, ejecutar manualmente (workflow_dispatch):

1. **Nuevo cliente** → `nuevo-cliente.yml`
2. **Modificar cliente** → `modificar-cliente.yml`
3. **Consulta** → `consulta-cliente.yml`
4. **Mejora** → Crear issue con label `mejora`
5. **Modificación código** → Push a branch `develop`
6. **Nueva función** → Crear issue con label `nueva-funcion`

## 4. AWS EC2 - Acceso desde cualquier lugar (3 min)

- Mostrar instancia t2.micro en consola AWS
- Mostrar usuarios IAM y grupos
- Abrir `http://<IP-EC2>/api/monitoreo/health` desde navegador
- Explicar que funciona desde casa, escuela, café, etc.

## 5. Control de versiones y rollback (3 min)

### Versión original vs nueva:
```bash
git tag v1.0.0
# Hacer cambio (ej: agregar endpoint /api/version)
git commit -m "feat: agregar endpoint de versión"
git tag v1.1.0
git push --tags
```

### Simular falla y rollback:
```bash
# En branch de prueba, borrar función vital en app.py (ej: health endpoint)
git commit -m "test: simular falla"
# Verificar que falla: curl health → error

# Rollback con GitHub:
git revert HEAD
# o: git checkout v1.0.0 -- sky_app/app.py
git push

# Redesplegar en EC2 y verificar que funciona de nuevo
```

## 6. Resumen final (1 min)

- DDD + microservicios + DevOps + CI/CD + AWS
- Cualquier miembro puede usar issues/workflows según su rol
- Versionado permite recuperar servicio ante fallas
