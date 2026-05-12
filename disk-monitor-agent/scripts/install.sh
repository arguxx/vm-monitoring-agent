#!/bin/bash
set -e


# Install Python and pip if not present (Ubuntu)
if ! command -v python3 >/dev/null 2>&1; then
    echo "Installing Python3..."
    sudo apt-get update
    sudo apt-get install -y python3
fi
if ! command -v pip3 >/dev/null 2>&1; then
    echo "Installing pip3..."
    sudo apt-get install -y python3-pip
fi

# Install dependencies
pip3 install -r $(dirname "$0")/../agent/requirements.txt

# Copy env example if not exists
if [ ! -f /etc/disk-agent.env ]; then
    cp $(dirname "$0")/../.env.example /etc/disk-agent.env
fi

# Copy systemd files
cp $(dirname "$0")/../systemd/*.service /etc/systemd/system/
cp $(dirname "$0")/../systemd/*.timer /etc/systemd/system/

# Enable and start services
systemctl daemon-reload
systemctl enable disk-agent.service disk-agent.timer disk-agent-update.service disk-agent-update.timer cpu-mem-agent.service cpu-mem-agent.timer
systemctl start disk-agent.timer disk-agent-update.timer cpu-mem-agent.timer

echo "Disk agent installed and started."
