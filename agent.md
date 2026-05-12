# Disk Monitor Agent with Telegram Alert

## Overview

Project ini bertujuan untuk membuat lightweight monitoring agent yang dipasang di setiap VM untuk:

- Monitoring disk usage
- Mengirim report harian ke Telegram
- Mengirim alert jika disk usage melewati threshold
- Auto update source code dari GitLab
- Berjalan autonomous tanpa central management server

---

# Architecture

```text
GitLab Repository
        │
   git pull/update
        │
 ┌──────┼──────┐
 │      │      │
VM-1  VM-2  VM-3
 │      │      │
Agent Agent Agent
 │      │      │
 └──────┼──────┘
        │
 Telegram Bot
```

---

# Features

## Monitoring
- Disk usage monitoring
- Multi mountpoint support
- Threshold alert
- Daily report

## Deployment
- Git-based deployment
- Auto update from GitLab
- Systemd service & timer
- No centralized server required

## Telegram
- Send alert to group
- Support Telegram Thread ID
- Hostname & IP information
- Markdown formatted message

---

# Project Structure

```text
disk-monitor-agent/
├── agent/
│   ├── disk_check.py
│   ├── requirements.txt
│   └── config.py
│
├── scripts/
│   ├── install.sh
│   └── update.sh
│
├── systemd/
│   ├── disk-agent.service
│   ├── disk-agent.timer
│   ├── disk-agent-update.service
│   └── disk-agent-update.timer
│
├── .gitignore
├── README.md
└── .env.example
```

---

# Telegram Bot Setup

## 1. Create Bot

Open:

https://t.me/BotFather

Run:

```text
/newbot
```

Save:
- BOT_TOKEN

---

# Telegram Group Setup

## 1. Create Group

Create Telegram group.

## 2. Add Bot to Group

Add created bot into group.

## 3. Disable Privacy Mode

Open BotFather:

```text
/setprivacy
```

Select bot → Disable

---

# Get Chat ID

Send message to group.

Then run:

```bash
curl https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
```

Example response:

```json
"chat":{"id":-1001234567890,"title":"Infra Alert"}
```

Save:

```text
CHAT_ID=-1001234567890
```

---

# Get Telegram Thread ID

Jika menggunakan Telegram Topics / Threads.

## 1. Create Topic

Create topic inside Telegram group.

Example:
- Disk Alert
- Infra Monitoring

## 2. Send Message to Topic

Send any message inside topic.

## 3. Get Updates

Run:

```bash
curl https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
```

Find:

```json
"message_thread_id":123
```

Save:

```text
THREAD_ID=123
```

---

# Environment Variables

## `/etc/disk-agent.env`

```env
BOT_TOKEN=xxxxxxxx
CHAT_ID=-1001234567890
THREAD_ID=123

THRESHOLD=80

REPORT_TIME=07:00
```

---

# Python Requirements

## `requirements.txt`

```text
psutil
requests
python-dotenv
```

---

# Main Agent

## `agent/disk_check.py`

Responsibilities:
- Check disk usage
- Format message
- Send Telegram alert
- Detect threshold breach

---

# Telegram Send Example

```python
requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    json={
        "chat_id": CHAT_ID,
        "message_thread_id": THREAD_ID,
        "text": message,
        "parse_mode": "Markdown"
    },
    timeout=10
)
```

---

# Systemd Service

## `disk-agent.service`

```ini
[Unit]
Description=Disk Monitoring Agent

[Service]
Type=oneshot
EnvironmentFile=/etc/disk-agent.env
WorkingDirectory=/opt/disk-monitor-agent
ExecStart=/opt/disk-monitor-agent/venv/bin/python agent/disk_check.py
```

---

# Systemd Timer

## `disk-agent.timer`

```ini
[Unit]
Description=Run Disk Monitoring Daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

---

# Auto Update Service

## `disk-agent-update.service`

```ini
[Unit]
Description=Update Disk Agent

[Service]
Type=oneshot
WorkingDirectory=/opt/disk-monitor-agent
ExecStart=/opt/disk-monitor-agent/scripts/update.sh
```

---

# Auto Update Timer

## `disk-agent-update.timer`

```ini
[Unit]
Description=Auto Update Disk Agent

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
```

---

# Install Script

## `scripts/install.sh`

Responsibilities:
- Install dependency
- Create Python virtualenv
- Install pip package
- Copy systemd service
- Enable timers

---

# Update Script

## `scripts/update.sh`

Responsibilities:
- Git pull latest source
- Install/update dependency
- Restart service if needed

Example:

```bash
#!/bin/bash

cd /opt/disk-monitor-agent || exit 1

git pull

source venv/bin/activate

pip install -r agent/requirements.txt

systemctl daemon-reload
systemctl restart disk-agent.timer
```

---

# Installation Flow

## 1. Clone Repository

```bash
git clone https://gitlab.com/company/disk-monitor-agent.git \
/opt/disk-monitor-agent
```

---

## 2. Create Environment File

```bash
cp .env.example /etc/disk-agent.env
```

Edit:

```bash
vim /etc/disk-agent.env
```

---

## 3. Run Installer

```bash
cd /opt/disk-monitor-agent

bash scripts/install.sh
```

---

# Verification

## Check Timer

```bash
systemctl status disk-agent.timer
```

---

## Check Logs

```bash
journalctl -u disk-agent.service -f
```

---

## Manual Run

```bash
systemctl start disk-agent.service
```

---

# Alert Example

## Daily Report

```text
📊 Daily Disk Report

🖥 Hostname: vm-prod-01
🌐 IP: 10.10.10.10

/: 61%
/data: 72%
```

---

## Threshold Alert

```text
🚨 DISK ALERT

🖥 Hostname: vm-db-01
🌐 IP: 10.10.10.20

/data: 95%
```

---

# Recommended Enhancements

## Future Features

- CPU monitoring
- Memory monitoring
- Inode monitoring
- Docker monitoring
- Kubernetes node monitoring
- SSL expiry monitoring
- Backup status monitoring

---

# Security Best Practices

## Recommended

- Store Telegram token outside repository
- Use private GitLab repository
- Use least privilege user
- Use virtualenv
- Enable GitLab branch protection

---

# Recommended Branching

## Branch Usage

| Branch | Purpose |
|---|---|
| main | Stable production |
| develop | Testing |
| feature/* | Development |

---

# Recommended GitLab CI/CD

Future improvement:
- Python linting
- Unit test
- Auto release tagging
- Package build
- Security scan

---

# Final Recommendation

Recommended stack:

| Component | Recommendation |
|---|---|
| Language | Python |
| Scheduler | systemd timer |
| Deployment | Git pull |
| Notification | Telegram Bot |
| Config | Environment file |
| Update Method | Auto pull |