# Container image that runs your code
FROM python:3.8-buster

# Copies your code file from your action repository to the filesystem path `/` of the container

COPY . /lean-upgrade-action/

#COPY entrypoint.sh /entrypoint.sh
#COPY update_or_report_error.py /update_or_report_error.py

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/lean-upgrade-action/entrypoint.sh"]