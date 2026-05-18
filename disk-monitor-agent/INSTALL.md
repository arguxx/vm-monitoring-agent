# Installation Guide

This guide covers installation and startup of the VM Monitoring Agent.

## Prerequisites

- Linux system with systemd (Ubuntu/Debian/RHEL/CentOS)
- Python 3.6 or higher
- pip3
- Git (for auto-update feature)
- Root or sudo access

## Quick Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url> /opt/disk-monitor-agent
cd /opt/disk-monitor-agent
```

### 2. Configure Environment Variables

Create the environment file:

```bash
sudo cp .env.example /etc/disk-agent.env
sudo vim /etc/disk-agent.env
```

Edit the file with your values:

```env
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
THREAD_ID=optional_thread_id
THRESHOLD=80
CPU_THRESHOLD=80
MEM_THRESHOLD=80
REPORT_TIME=07:00
```

### 3. Run Installation Script

```bash
sudo bash scripts/install.sh
```

This script will:
- Install Python3 and pip3 if not present
- Install Python dependencies (psutil, requests, python-dotenv)
- Copy systemd service and timer files
- Enable and start all services

### 4. Verify Installation

Check timer status:

```bash
sudo systemctl status disk-agent.timer
sudo systemctl status cpu-mem-agent.timer
sudo systemctl status disk-agent-update.timer
```

Check service logs:

```bash
sudo journalctl -u disk-agent.service -f
sudo journalctl -u cpu-mem-agent.service -f
```

## Manual Installation

If you prefer manual installation:

### 1. Install Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip git
pip3 install -r agent/requirements.txt
```

### 2. Configure Environment

```bash
sudo cp .env.example /etc/disk-agent.env
sudo vim /etc/disk-agent.env
```

### 3. Install Systemd Services

Copy service files:

```bash
sudo cp systemd/*.service /etc/systemd/system/
sudo cp systemd/*.timer /etc/systemd/system/
```

**Important**: Edit the service files to update the paths:

Edit `/etc/systemd/system/disk-agent.service`:
```ini
ExecStart=/usr/bin/python3 /opt/disk-monitor-agent/agent/disk_check.py
```

Edit `/etc/systemd/system/cpu-mem-agent.service`:
```ini
ExecStart=/usr/bin/python3 /opt/disk-monitor-agent/agent/cpu_mem_check.py
```

Edit `/etc/systemd/system/disk-agent-update.service`:
```ini
ExecStart=/bin/bash /opt/disk-monitor-agent/scripts/update.sh
```

### 4. Enable and Start Services

```bash
sudo systemctl daemon-reload
sudo systemctl enable disk-agent.service disk-agent.timer
sudo systemctl enable cpu-mem-agent.service cpu-mem-agent.timer
sudo systemctl enable disk-agent-update.service disk-agent-update.timer
sudo systemctl start disk-agent.timer cpu-mem-agent.timer disk-agent-update.timer
```

## Starting and Stopping

### Start Services

```bash
sudo systemctl start disk-agent.timer
sudo systemctl start cpu-mem-agent.timer
sudo systemctl start disk-agent-update.timer
```

### Stop Services

```bash
sudo systemctl stop disk-agent.timer
sudo systemctl stop cpu-mem-agent.timer
sudo systemctl stop disk-agent-update.timer
```

### Restart Services

```bash
sudo systemctl restart disk-agent.timer
sudo systemctl restart cpu-mem-agent.timer
sudo systemctl restart disk-agent-update.timer
```

### Disable Services (on boot)

```bash
sudo systemctl disable disk-agent.timer
sudo systemctl disable cpu-mem-agent.timer
sudo systemctl disable disk-agent-update.timer
```

## Manual Testing

### Test Disk Check

```bash
cd /opt/disk-monitor-agent
python3 agent/disk_check.py
```

### Test CPU/Memory Check

```bash
python3 agent/cpu_mem_check.py
```

### Send Daily Report Manually

```bash
python3 agent/disk_check.py report
python3 agent/cpu_mem_check.py report
```

## Using Cron Instead of Systemd

If you prefer cron over systemd timers:

### 1. Disable Systemd Timers

```bash
sudo systemctl stop disk-agent.timer cpu-mem-agent.timer disk-agent-update.timer
sudo systemctl disable disk-agent.timer cpu-mem-agent.timer disk-agent-update.timer
```

### 2. Edit Crontab

```bash
crontab -e
```

Add these lines (adjust paths as needed):

```cron
# Check disk every 5 minutes
*/5 * * * * /usr/bin/python3 /opt/disk-monitor-agent/agent/disk_check.py

# Check CPU/memory every 5 minutes
*/5 * * * * /usr/bin/python3 /opt/disk-monitor-agent/agent/cpu_mem_check.py

# Daily report at 07:00
0 7 * * * /usr/bin/python3 /opt/disk-monitor-agent/agent/disk_check.py report
0 7 * * * /usr/bin/python3 /opt/disk-monitor-agent/agent/cpu_mem_check.py report

# Auto-update daily at 06:00
0 6 * * * /bin/bash /opt/disk-monitor-agent/scripts/update.sh
```

## Troubleshooting

### Service Not Starting

Check logs:
```bash
sudo journalctl -u disk-agent.service -n 50
sudo journalctl -u cpu-mem-agent.service -n 50
```

Common issues:
- Wrong Python path in service file
- Missing dependencies
- Incorrect environment file location
- Permission issues

### Telegram Alerts Not Sending

1. Verify BOT_TOKEN and CHAT_ID in `/etc/disk-agent.env`
2. Check if bot is added to the group
3. Verify bot privacy mode is disabled (use BotFather)
4. Check service logs for error messages

### Auto-Update Not Working

1. Verify Git repository is properly cloned
2. Check if git is installed: `which git`
3. Verify update script has correct path
4. Check update service logs: `sudo journalctl -u disk-agent-update.service -n 50`

### Wrong Paths in Systemd Files

The current systemd files have hardcoded paths. Update them:

```bash
sudo vim /etc/systemd/system/disk-agent.service
sudo vim /etc/systemd/system/cpu-mem-agent.service
sudo vim /etc/systemd/system/disk-agent-update.service
```

Change `/root/vm-monitoring-agent/` to your actual installation path (e.g., `/opt/disk-monitor-agent/`).

Then reload:

```bash
sudo systemctl daemon-reload
sudo systemctl restart disk-agent.timer cpu-mem-agent.timer
```

## Uninstallation

### Stop and Disable Services

```bash
sudo systemctl stop disk-agent.timer cpu-mem-agent.timer disk-agent-update.timer
sudo systemctl disable disk-agent.timer cpu-mem-agent.timer disk-agent-update.timer
```

### Remove Service Files

```bash
sudo rm /etc/systemd/system/disk-agent.service
sudo rm /etc/systemd/system/disk-agent.timer
sudo rm /etc/systemd/system/cpu-mem-agent.service
sudo rm /etc/systemd/system/cpu-mem-agent.timer
sudo rm /etc/systemd/system/disk-agent-update.service
sudo rm /etc/systemd/system/disk-agent-update.timer
sudo systemctl daemon-reload
```

### Remove Environment File

```bash
sudo rm /etc/disk-agent.env
```

### Remove Project Directory

```bash
sudo rm -rf /opt/disk-monitor-agent
```

## Next Steps

- See [CUSTOMIZE.md](CUSTOMIZE.md) for customization options
- See [agent.md](agent.md) for detailed architecture and Telegram setup
