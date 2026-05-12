# Disk Monitor Agent

A lightweight agent for monitoring disk, CPU, and memory usage and sending alerts/reports to Telegram.

## Features

- Disk usage monitoring (multi-mountpoint)
- CPU usage monitoring
- Memory usage monitoring
- Telegram alert if any threshold exceeded
- Daily report to Telegram
- Auto update from GitLab
- Systemd service & timer
- No central server required

## Usage

- Configure `/etc/disk-agent.env` or `.env` with your Telegram and threshold settings.
- Run `python disk_check.py` to check disk and send alert if needed.
- Run `python cpu_mem_check.py` to check CPU/memory and send alert if needed.
- Use systemd timer for daily report and auto-update.

See agent.md for full details.
