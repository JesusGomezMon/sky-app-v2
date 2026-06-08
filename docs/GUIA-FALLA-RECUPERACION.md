# Simulacion de Falla y Recuperacion - SKY App v2.0

Guia para documentar Figuras 19, 20 y 21.

---

## Versiones de referencia

| Tag/Commit | Estado | Descripcion |
|------------|--------|-------------|
| `v1.0.0` | Estable | Version funcional original |
| `test/falla-simulada` | Rota | Simula falla (app no arranca) |
| `main` | Estable | Version actual con CRUD y validacion |

---

## PARTE A — Simulacion LOCAL (tu PC)

### Paso 1 — Verificar que funciona (ANTES)

```powershell
cd "C:\Users\Jesus Gomez\Desktop\DevOps\fase2"
git checkout main
python sky_app/app.py
```

Otra terminal:
```powershell
curl http://127.0.0.1:5000/api/monitoreo/health
```

**Captura Figura 21 (antes):** respuesta `{"status":"ok"}`

---

### Paso 2 — Simular la falla

```powershell
git checkout test/falla-simulada
python sky_app/app.py
```

**Captura Figura 19:** Error en terminal (SyntaxError o app no responde)

Otra terminal:
```powershell
curl http://127.0.0.1:5000/api/monitoreo/health
```
Debe fallar (connection refused o error).

---

### Paso 3 — Restaurar version anterior

```powershell
git checkout v1.0.0
# o: git checkout main
python sky_app/app.py
```

Otra terminal:
```powershell
curl http://127.0.0.1:5000/api/monitoreo/health
```

**Captura Figura 20:** comando `git checkout v1.0.0` en terminal
**Captura Figura 21 (despues):** health responde OK de nuevo

---

## PARTE B — Simulacion en AWS EC2 (opcional, mas impresionante)

### Paso 1 — Verificar que funciona

```bash
curl http://localhost/api/monitoreo/health
```

Navegador: `http://18.217.68.203/api/monitoreo/health`

---

### Paso 2 — Aplicar version rota

```bash
cd /home/ec2-user/sky-app-v2
git fetch origin
git checkout test/falla-simulada
sudo cp sky_app/app.py /opt/sky-app/sky_app/app.py
sudo systemctl restart sky-app
sleep 2
curl http://localhost/api/monitoreo/health
```

**Captura Figura 19:** curl falla o `systemctl status sky-app` muestra error

---

### Paso 3 — Restaurar con Git

```bash
cd /home/ec2-user/sky-app-v2
git checkout v1.0.0
sudo cp sky_app/app.py /opt/sky-app/sky_app/app.py
sudo systemctl restart sky-app
sleep 2
curl http://localhost/api/monitoreo/health
```

**Captura Figura 20:** `git checkout v1.0.0`
**Captura Figura 21:** health OK + navegador funciona

---

## Texto para tu documento

### Paso 1
Se elimino el bloque de arranque del servidor en `app.py` (seccion critica).
**Resultado:** La aplicacion dejo de funcionar.

### Paso 2
Se restauro la version estable con:
```bash
git checkout v1.0.0
```

### Paso 3
Se verifico la ejecucion con `curl http://localhost/api/monitoreo/health`
**Resultado:** Sistema restaurado correctamente.

---

## Comandos Git utiles para capturas

```bash
git log --oneline -5          # ver historial
git checkout test/falla-simulada # version rota
git checkout v1.0.0           # restaurar
git tag -l                    # ver versiones
```
