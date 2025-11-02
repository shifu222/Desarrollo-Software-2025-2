# Actividad13-CC3S2 — Infraestructura como código local con Terraform

Este repositorio contiene la solución de la Actividad 13: un generador Python que crea entornos locales Terraform en JSON a partir de plantillas.

Estructura principal

- `modules/simulated_app/`
  - `network.tf.json` — plantilla de variables (network default `lab-net`, `port`, `api_key` marcado `sensitive`).
  - `main.tf.json` — recursos (renombrado `null_resource` -> `local_server`).
- `environments/` — generados por `generate_envs.py`: `app1`, `app2`, `env3`.
- `legacy/` — ejemplo legacy con `config.cfg` y `run.sh`.
- `generate_envs.py` — generador principal (lee plantillas y escribe entornos; no escribe `api_key`).
- `scripts/gitops_regenerate.sh` — regenerador simple.

Cómo usar

1. Instalar dependencias de python: `pip install -r requirements.txt`.
2. Ejecutar el generador:

```powershell
python .\Actividad13-CC3S2\generate_envs.py
```

3. Entrar en un entorno y ejecutar Terraform :

```powershell
cd .\Actividad13-CC3S2\environments\app1
terraform init
terraform plan
```

Notas sobre secretos

- `api_key` está definido como variable `sensitive` en las plantillas. El script detecta si existe `API_KEY` o `TF_VAR_api_key` en las variables de entorno y no lo escribe en disco. Para que Terraform lo use en `plan`/`apply`, exporte la variable `TF_VAR_api_key` en su shell.
- No versionar `~/.config/secure.json` ni ficheros con secretos.

## Ronda de Preguntas

### - Respuestas (Fase 1)

- ¿Cómo interpreta Terraform el cambio de variable?
  - Terraform compara la configuración generada con el estado, y las variables que se usan en `triggers` de recursos (`null_resource`/`local_server`) producen diferencias en `triggers` cuando cambian sus valores. El `plan` mostrará `~ null_resource... triggers.network: "old" -> "new"`.

- ¿Qué diferencia hay entre modificar el JSON vs parchear directamente el recurso?
  - Si cambias la plantilla (fuente) y la regeneras, la modificación queda reproducible y formateada; Terraform detecta el cambio en los valores y puede aplicar remediación. Si editas directamente el `main.tf.json` (out-of-band), Terraform detectará drift y propondrá revertirlo en `plan` (ya que el estado o la plantilla no coincide). Editar la plantilla es la vía correcta para mantener IaC como autoridad.

- ¿Por qué Terraform no recrea todo el recurso, sino que aplica el cambio "in-place"?
  - Terraform decide recrear o modificar en función del tipo de recurso y de qué atributos se han marcado como que requieren recreación. Para `null_resource` los `triggers` son metadatos que forzan reprovisiones si cambian, pero no implican necesariamente eliminar/crear recursos reales: Terraform sólo actualiza el recurso en su plan (reprovisionar en lugar de recrear completamente) si la semántica del proveedor/ recurso lo permite.

- ¿Qué pasa si editas directamente `main.tf.json` en lugar de la plantilla de variables?
  - Editar directamente genera drift detectado por `terraform plan`, que propondrá revertir los cambios si la fuente de la verdad es la plantilla regenerada. Además, editar manualmente rompe reproducibilidad y el histórico de cambios.

### - Respuestas(Fase 4) — propuestas prácticas

- ¿Cómo extenderías para 50 módulos y 100 entornos?
  - Crear plantillas modulares con parámetros, una base de datos de parámetros por entorno, pipeline CI que ejecute validación y generación, y un naming convention para recursos. Automatizar generación y pruebas en paralelo.

- ¿Qué prácticas de revisión aplicarías a los `.tf.json`?
  - Validación con JSON Schema, formato con `jq`, hooks pre-commit, PRs con `terraform plan` en CI y reglas para variables sensibles.

- ¿Cómo gestionar secretos en producción (sin Vault)?
  - Usar almacenamientos de secretos cifrados (ej. archivos cifrados GPG), variables de entorno en CI con acceso controlado, o servicios secretos del proveedor. Evitar versionar secretos; establecer auditoría.

- ¿Qué workflows de revisión aplicarías a los JSON generados?
  - No recomendar revisar manualmente JSON generados; en su lugar, revisar plantillas y el generador. Validar outputs en CI (jq, jsonschema, terraform plan). Autogenerar diffs y adjuntarlos al PR.

Ejercicios implementados

- Generador Python que crea `app1`, `app2`, `env3`.
- `network.tf.json` en plantillas ajustado con `network` default `lab-net`, `port` y `api_key` sensitive.
- `main.tf.json` con recurso renombrado a `local_server`.
- `legacy/` con `config.cfg` y `run.sh`.
- Script `gitops_regenerate.sh`.

Archivos importantes añadidos

- `Actividad13-CC3S2/generate_envs.py` — generador principal.
- `Actividad13-CC3S2/modules/simulated_app/network.tf.json` — variables.
- `Actividad13-CC3S2/modules/simulated_app/main.tf.json` — recurso.
- `Actividad13-CC3S2/environments/{app1,app2,env3}/` — generados por el script.
- `Actividad13-CC3S2/legacy/` — legacy example.

Cómo validar rápido

1. Ejecutar el generador (ya incluido):

```powershell
python .\Actividad13-CC3S2\generate_envs.py
```

2. Ir a `environments/app1`, ejecutar `terraform init` y `terraform plan` (si tiene Terraform).

Notas finales

- No incluí `secure.json` en el repo. Colóquelo en `~/.config/secure.json` y exporte `TF_VAR_api_key` para que Terraform lo utilice en `plan`/`apply`.
