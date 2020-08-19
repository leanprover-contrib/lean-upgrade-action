#!/bin/bash -l

PATH="$PATH:/root/.elan/bin"
python /lean-upgrade-action/update_or_report_error.py "$1" "$2"