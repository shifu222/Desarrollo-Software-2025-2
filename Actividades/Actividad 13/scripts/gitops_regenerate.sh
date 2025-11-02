#!/bin/bash
# Script simple para regenerar todos los entornos cuando modules/simulated_app/ cambia
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT_DIR/generate_envs.py"
