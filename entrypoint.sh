#!/bin/bash -l

PATH="$PATH:$HOME/.elan/bin"
python /lean-upgrade-action/update_or_report_error.py "$1" "$2" || exit 1

git config user.email "leanprover.community@gmail.com"
git config user.name "leanprover-community-bot"
git add leanpkg.toml
git commit -m "auto update dependencies"
git push "$3"