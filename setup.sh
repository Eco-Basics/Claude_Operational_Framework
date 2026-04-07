#!/usr/bin/env bash
# setup.sh — Bootstrap Claude Operational Framework on a new machine or VPS
# Usage: bash ~/.claude/setup.sh
# Assumes: git and python3 are available

set -euo pipefail

CLAUDE_HOME="$HOME/.claude"
REPO="https://github.com/Eco-Basics/Claude_Operational_Framework"

echo "=== Claude Framework Bootstrap ==="
echo "Machine: $(uname -s) $(uname -m)"
echo "Home: $HOME"
echo ""

# --- 1. Clone or verify repo ---
if [ -d "$CLAUDE_HOME/.git" ]; then
    echo "[OK] ~/.claude is already a git repo"
    echo "     Pulling latest..."
    git -C "$CLAUDE_HOME" pull --ff-only
else
    echo "[SETUP] Cloning framework to ~/.claude..."
    git clone "$REPO" "$CLAUDE_HOME"
fi

# --- 2. Verify Python ---
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 --version 2>&1)
    echo "[OK] Python: $PY_VER"
else
    echo "[ERROR] python3 not found. Install Python 3.8+ and re-run."
    exit 1
fi

# --- 3. Create required runtime directories ---
mkdir -p "$CLAUDE_HOME/agent-logs"
mkdir -p "$CLAUDE_HOME/memory/worker-profiles"
echo "[OK] Runtime directories ready"

# --- 4. Make skill scripts executable ---
find "$CLAUDE_HOME/skills" -name "*.py" -exec chmod +x {} \;
echo "[OK] Skill scripts executable"

# --- 5. Machine-specific settings reminder ---
if [ ! -f "$CLAUDE_HOME/settings.local.json" ]; then
    echo ""
    echo "[NOTE] settings.local.json not found."
    echo "       Create it manually — it is gitignored and machine-specific."
    echo "       Minimum content: {}"
fi

echo ""
echo "=== Bootstrap complete ==="
echo "Framework at: $CLAUDE_HOME"
echo "Next: open Claude Code and run /intent to start a project."
