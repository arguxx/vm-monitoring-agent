# Disk Monitor Agent

A lightweight agent for monitoring disk usage and sending alerts/reports to Telegram.

## Features

- Disk usage monitoring (multi-mountpoint)
- Telegram alert if threshold exceeded
- Daily report to Telegram
- Auto update from GitLab
- Systemd service & timer
- No central server required

## Project Structure

```
disk-monitor-agent/
├── agent/
│   ├── disk_check.py
│   ├── cpu_mem_check.py
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

## Setup

1. Copy `.env.example` to `/etc/disk-agent.env` and fill in your values.
2. Run `scripts/install.sh` as root.

3. Check Telegram for alerts and reports.

## How to Change Schedule (Cron)

You can use cron to schedule the agent scripts:

1. Open your crontab editor:
    ```
    crontab -e
    ```
2. Add lines like these (adjust paths as needed):
    - Run disk check every 5 minutes:
        ```
        */5 * * * * /usr/bin/python3 /path/to/disk-monitor-agent/agent/disk_check.py
        ```
    - Run CPU/memory check every 5 minutes:
        ```
        */5 * * * * /usr/bin/python3 /path/to/disk-monitor-agent/agent/cpu_mem_check.py
        ```
    - Run daily report at 07:00:
        ```
        0 7 * * * /usr/bin/python3 /path/to/disk-monitor-agent/agent/disk_check.py report
        0 7 * * * /usr/bin/python3 /path/to/disk-monitor-agent/agent/cpu_mem_check.py report
        ```

## How to Change Thresholds

Edit your `/etc/disk-agent.env` or `.env` file:

- For disk usage threshold:
    ```
    THRESHOLD=80
    ```
- For CPU usage threshold:
    ```
    CPU_THRESHOLD=80
    ```
- For memory usage threshold:
    ```
    MEM_THRESHOLD=80
    ```

After changing the values, the new thresholds will be used the next time the script runs.

## CPU/Memory Agent

- Configure `CPU_THRESHOLD` and `MEM_THRESHOLD` in your env file.
- Run `python agent/cpu_mem_check.py` for CPU/memory monitoring.

See agent.md for full details and Telegram setup instructions.
