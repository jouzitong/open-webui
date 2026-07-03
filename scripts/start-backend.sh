#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv}"
REQUIREMENTS_FILE="${OPEN_WEBUI_BACKEND_REQUIREMENTS:-$BACKEND_DIR/requirements.txt}"
REQUIRED_PYTHON_MINOR="${REQUIRED_PYTHON_MINOR:-11}"

load_env_file() {
  local file="$1"
  if [[ -f "$file" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$file"
    set +a
  fi
}

pick_python() {
  local candidates=()
  local python_bin version

  if [[ -x "$HOME/.local/python-3.11.15/bin/python3.11" ]]; then
    candidates+=("$HOME/.local/python-3.11.15/bin/python3.11")
  fi

  if command -v python3.11 >/dev/null 2>&1; then
    candidates+=("$(command -v python3.11)")
  fi
  if command -v python3.12 >/dev/null 2>&1; then
    candidates+=("$(command -v python3.12)")
  fi
  if command -v python3 >/dev/null 2>&1; then
    candidates+=("$(command -v python3)")
  fi
  if command -v python >/dev/null 2>&1; then
    candidates+=("$(command -v python)")
  fi

  for python_bin in "${candidates[@]}"; do
    version="$("$python_bin" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || true)"
    if [[ "$version" =~ ^3\.([0-9]+)$ ]] && [[ "${BASH_REMATCH[1]}" -ge "$REQUIRED_PYTHON_MINOR" ]]; then
      echo "$python_bin"
      return 0
    fi
  done

  echo "Python 3.${REQUIRED_PYTHON_MINOR}+ is required for Open WebUI backend." >&2
  echo "Current system Python: $(python3 --version 2>/dev/null || python --version 2>/dev/null || echo "not found")" >&2
  echo "Install Python 3.11 first, then rerun this script." >&2
  exit 1
}

ensure_python_version() {
  local python_bin="$1"
  local version
  version="$("$python_bin" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')"
  echo "Using Python $version"
}

backup_incompatible_venv() {
  local backup_dir="${VENV_DIR}.bak.$(date +%Y%m%d%H%M%S)"
  echo "Existing virtualenv is incompatible. Backing it up to $backup_dir"
  mv "$VENV_DIR" "$backup_dir"
}

ensure_compatible_venv() {
  if [[ ! -x "$VENV_DIR/bin/python" ]]; then
    return 0
  fi

  local venv_version
  venv_version="$("$VENV_DIR/bin/python" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || true)"
  if [[ ! "$venv_version" =~ ^3\.([0-9]+)$ ]] || [[ "${BASH_REMATCH[1]}" -lt "$REQUIRED_PYTHON_MINOR" ]]; then
    backup_incompatible_venv
  fi
}

ensure_backend_venv() {
  local python_bin="$1"

  ensure_compatible_venv

  if [[ ! -x "$VENV_DIR/bin/python" ]]; then
    echo "Creating virtualenv at $VENV_DIR"
    "$python_bin" -m venv "$VENV_DIR"
  fi

  # Keep the bootstrap simple: install on first run or when the caller removes the marker.
  if [[ ! -f "$VENV_DIR/.open-webui-backend-ready" ]]; then
    echo "Installing backend dependencies from $REQUIREMENTS_FILE"
    "$VENV_DIR/bin/pip" install --upgrade pip
    "$VENV_DIR/bin/pip" install -r "$REQUIREMENTS_FILE"
    touch "$VENV_DIR/.open-webui-backend-ready"
  fi
}

main() {
  cd "$ROOT_DIR"

  load_env_file "$ROOT_DIR/.env.example"
  load_env_file "$ROOT_DIR/.env"
  load_env_file "$ROOT_DIR/.env.local"

  export HOST="${HOST:-0.0.0.0}"
  export PORT="${PORT:-8080}"

  local python_bin
  python_bin="$(pick_python)"
  ensure_python_version "$python_bin"
  ensure_backend_venv "$python_bin"

  source "$VENV_DIR/bin/activate"

  echo "Starting Open WebUI backend on http://$HOST:$PORT"
  exec "$BACKEND_DIR/start.sh" "$@"
}

main "$@"
