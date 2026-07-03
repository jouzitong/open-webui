#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

load_env_file() {
  local file="$1"
  if [[ -f "$file" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$file"
    set +a
  fi
}

prefer_compatible_node() {
  local candidate_bin_dirs=(
    "$HOME/.nvm/versions/node/v22.*/bin"
    "$HOME/.nvm/versions/node/v20.*/bin"
    "/opt/homebrew/opt/node@22/bin"
    "/opt/homebrew/opt/node@20/bin"
    "/usr/local/opt/node@22/bin"
    "/usr/local/opt/node@20/bin"
  )

  local current_major
  current_major="$(node -p 'process.versions.node.split(\".\")[0]' 2>/dev/null || echo "")"
  if [[ -n "$current_major" && "$current_major" -ge 18 && "$current_major" -le 22 ]]; then
    return 0
  fi

  local pattern dir
  for pattern in "${candidate_bin_dirs[@]}"; do
    for dir in $pattern; do
      if [[ -x "$dir/node" && -x "$dir/npm" ]]; then
        export PATH="$dir:$PATH"
        hash -r
        return 0
      fi
    done
  done
}

ensure_supported_node() {
  local node_version node_major npm_version
  node_version="$(node -v 2>/dev/null || true)"
  npm_version="$(npm -v 2>/dev/null || true)"
  node_major="$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo "")"

  if [[ -z "$node_major" || "$node_major" -lt 18 || "$node_major" -gt 22 ]]; then
    echo "Unsupported Node.js version: ${node_version:-unknown} (npm ${npm_version:-unknown})" >&2
    echo "Open WebUI requires Node.js >=18.13.0 and <=22.x." >&2
    echo "If you use nvm, switch first: nvm use 22" >&2
    exit 1
  fi

  # The current lockfile pulls packages that require at least Node 20.19 or 22.13
  # when engine-strict is enabled in this repo.
  local node_minor
  node_minor="$(node -p 'process.versions.node.split(".").slice(1,2)[0]' 2>/dev/null || echo "")"
  if [[ "$node_major" == "20" && -n "$node_minor" && "$node_minor" -lt 19 ]]; then
    echo "Node.js ${node_version} is too old for the current lockfile when engine-strict=true." >&2
    echo "Use Node 20.19+ or Node 22.13+." >&2
    exit 1
  fi
}

has_frontend_dependencies() {
  [[ -d "$ROOT_DIR/node_modules" ]] \
    && [[ -x "$ROOT_DIR/node_modules/.bin/vite" ]] \
    && [[ -x "$ROOT_DIR/node_modules/.bin/svelte-kit" ]]
}

ensure_frontend_dependencies() {
  if has_frontend_dependencies; then
    return 0
  fi

  echo "Installing frontend dependencies with npm install"
  echo "Skipping Cypress binary download during setup; run 'npx cypress install' later if needed."
  CYPRESS_INSTALL_BINARY="${CYPRESS_INSTALL_BINARY:-0}" npm install
}

main() {
  cd "$ROOT_DIR"

  load_env_file "$ROOT_DIR/.env.example"
  load_env_file "$ROOT_DIR/.env"
  load_env_file "$ROOT_DIR/.env.local"

  if ! command -v npm >/dev/null 2>&1; then
    echo "npm not found. Install Node.js 18-22 first." >&2
    exit 1
  fi

  prefer_compatible_node
  ensure_supported_node

  ensure_frontend_dependencies

  local port="${PORT:-5173}"
  echo "Using Node $(node -v) / npm $(npm -v)"
  echo "Starting Open WebUI frontend on http://127.0.0.1:$port"

  if [[ "$#" -gt 0 ]]; then
    exec npm run dev -- "$@"
  else
    exec npm run dev -- --port "$port"
  fi
}

main "$@"
