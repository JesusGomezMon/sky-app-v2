# Subir proyecto a GitHub (tu cuenta)

El repositorio ya fue creado en: **https://github.com/JesusGomezMon/sky-app-v2**

## Paso 1: Autorizar permisos de workflow

GitHub requiere el scope `workflow` para subir archivos de Actions.

1. Abre: https://github.com/login/device
2. Ingresa el codigo que muestra `gh auth refresh`
3. O ejecuta en terminal:

```powershell
gh auth refresh -h github.com -s workflow,repo
```

## Paso 2: Push del codigo

```powershell
cd "C:\Users\Jesus Gomez\Desktop\DevOps\fase2"
git push -u origin main
git tag v1.0.0
git push origin v1.0.0
```

## Paso 3: Agregar miembros del equipo

En GitHub → **Settings → Collaborators and teams → Add people**

| Usuario | Rol GitHub | Equipo DevOps |
|---------|------------|---------------|
| dev1 | Admin | Desarrollador 1 |
| dev2 | Admin | Desarrollador 2 |
| it1 | Maintain | IT 1 |
| it2 | Maintain | IT 2 |
| atencion1 | Triage | Atencion 1 |
| atencion2 | Triage | Atencion 2 |

> El repositorio esta en **tu cuenta** (JesusGomezMon). Tu eres el owner.

## Paso 4: Simular falla y rollback (para el video)

```powershell
git checkout -b feature/version-endpoint
git commit -am "feat: agregar endpoint version"
git tag v1.1.0

git checkout -b test/falla-simulada
git commit -am "test: simular falla en health endpoint"

git checkout main
git revert HEAD
git push
```
