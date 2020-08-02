#!/bin/sh -l

python -m pip install --upgrade pip mathlibtools
curl https://raw.githubusercontent.com/Kha/elan/master/elan-init.sh -sSf | sh -s -- -y
PATH="$PATH:$HOME/.elan/bin"
python update_or_report_error.py 

branch_name="lean-$(grep -oP 'lean_version = \"leanprover-community\/lean\:\K[^\=]+(?=\")' leanpkg.toml)"
echo "Updating mathlib branch $branch_name to match master"
git push "$1" HEAD:refs/heads/$branch_name