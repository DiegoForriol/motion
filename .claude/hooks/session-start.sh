#!/bin/bash
set -euo pipefail

# Only run in remote (web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

echo "Installing claude-seo skills..."

INSTALL_DIR=$(mktemp -d)
trap "rm -rf ${INSTALL_DIR}" EXIT

git clone --depth 1 https://github.com/AgriciDaniel/claude-seo.git "${INSTALL_DIR}/claude-seo" 2>&1
bash "${INSTALL_DIR}/claude-seo/install.sh"
