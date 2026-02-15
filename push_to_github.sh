#!/usr/bin/env bash
# Run this script from the SmartAssist folder in your system terminal
# to commit and push to https://github.com/lokanath93/SmartAssist
# Usage: ./push_to_github.sh   or   bash push_to_github.sh

set -e
cd "$(dirname "$0")"

echo "=== SmartAssist: push to GitHub ==="
echo ""

# 1. Create repo on GitHub first: https://github.com/new , name: SmartAssist (no README/license)
# 2. Then run this script.

git add .gitignore README.md requirements.txt main.py
git status
echo ""
read -p "Commit and push? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Aborted."
  exit 0
fi

git commit -m "Initial commit: SmartAssist head mouse blink click voice typing"
git branch -M main

if ! git remote get-url origin 2>/dev/null; then
  git remote add origin https://github.com/lokanath93/SmartAssist.git
fi

git push -u origin main
echo ""
echo "Done. Repo: https://github.com/lokanath93/SmartAssist"
