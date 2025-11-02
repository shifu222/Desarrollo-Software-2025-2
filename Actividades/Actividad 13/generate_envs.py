#!/usr/bin/env python3
"""
Generador de entornos
- Usa las plantillas en modules/simulated_app/
- Genera environments/app1, app2, env3
- No escribe api_key en disco
- CLI con click: --count, --prefix, --port
"""
import os
import json
import shutil
from pathlib import Path

try:
    import click
except Exception:
    click = None

ROOT = Path(__file__).resolve().parent
MODULES = ROOT / "modules" / "simulated_app"
ENV_DIR = ROOT / "environments"

DEFAULT_ENVS = [
    {"name": "app1", "network": "lab-net", "port": 8080},
    {"name": "app2", "network": "net2", "port": 8081},
    {"name": "env3", "network": "net2-peered", "port": 8082},
]


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)


def simple_validate_tf_json(obj):
    # válido si contiene la clave  'variable' o 'resource'
    if not isinstance(obj, dict):
        return False
    if 'variable' in obj or 'resource' in obj:
        return True
    return False


def generate(envs):
    # cargar plantillas
    tpl_network = load_json(MODULES / "network.tf.json")
    tpl_main = load_json(MODULES / "main.tf.json")

    # detectar api_key en las variables de entorno
    api_key = os.environ.get('API_KEY') or os.environ.get('TF_VAR_api_key')
    if api_key:
        print("Se detectó API_KEY en variables de entorno — no se escribirá en disco")

    for e in envs:
        name = e['name']
        dest = ENV_DIR / name
        dest.mkdir(parents=True, exist_ok=True)

        net = dict(tpl_network)

        variables = json.loads(json.dumps(tpl_network.get('variable', {})))
        if 'network' in variables:
            variables['network']['default'] = e['network']
        else:
            variables['network'] = {"type": "string", "default": e['network']}
        if 'port' in variables:
            variables['port']['default'] = e['port']
        else:
            variables['port'] = {"type": "number", "default": e['port']}

        if 'api_key' in variables:
            variables['api_key'].pop('default', None)
            variables['api_key']['sensitive'] = True
        else:
            variables['api_key'] = {"type": "string", "sensitive": True}

        net['variable'] = variables
        write_json(dest / 'network.tf.json', net)

        main = dict(tpl_main)

        write_json(dest / 'main.tf.json', main)

        print(f"Generated environment: {name} -> {dest}")

    print('\nResumen:')
    print(f'  Envs escritos en: {ENV_DIR}')
    print('  api_key  debe proporcionarse a Terraform mediante TF_VAR_api_key o variables de entorno')


if click:
    @click.command()
    @click.option('--count', default=3, help='Número de entornos a generar')
    @click.option('--prefix', default='', help='Prefijo para nombres (ej: staging -> staging1, staging2)')
    @click.option('--port', default=8080, help='Puerto base (se incrementa por entorno)')
    def cli(count, prefix, port):
        envs = []
        for i in range(1, min(count, 50) + 1):
            idx = i - 1
            name = f"{prefix}{i}" if prefix else DEFAULT_ENVS[idx % len(
                DEFAULT_ENVS)]['name']
            network = DEFAULT_ENVS[idx % len(DEFAULT_ENVS)]['network']
            p = port + (i - 1)
            envs.append({'name': name, 'network': network, 'port': p})
        generate(envs)

    if __name__ == '__main__':
        cli()
else:
    if __name__ == '__main__':
        generate(DEFAULT_ENVS)
