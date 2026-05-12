#!/bin/bash
set -e

cd $(dirname "$0")/..
git pull
pip install -r agent/requirements.txt
systemctl restart disk-agent.service
