#!/bin/sh -l

python -m pip install --upgrade pip mathlibtools
curl https://raw.githubusercontent.com/Kha/elan/master/elan-init.sh -sSf | sh -s -- -y
PATH="$PATH:$HOME/.elan/bin"
python update_or_report_error.py "${{ github.repository }}" "$1"

git config user.email "leanprover.community@gmail.com"
git config user.name "leanprover-community-bot"
git add leanpkg.toml
git commit -m "auto update dependencies"
git push "$2"