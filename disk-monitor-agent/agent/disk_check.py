import psutil
import socket
import requests
import os
from datetime import datetime
from config import BOT_TOKEN, CHAT_ID, THREAD_ID, THRESHOLD


def get_hostname_ip():
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except Exception:
        ip = 'Unknown'
    return hostname, ip


def get_disk_usage():
    usage = []
    for part in psutil.disk_partitions():
        if os.name == 'nt' or part.fstype == '':
            continue
        try:
            du = psutil.disk_usage(part.mountpoint)
            usage.append({
                'mountpoint': part.mountpoint,
                'total': du.total,
                'used': du.used,
                'free': du.free,
                'percent': du.percent
            })
        except Exception:
            continue
    return usage


def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown',
    }
    if THREAD_ID:
        data['message_thread_id'] = THREAD_ID
    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print(f"Failed to send alert: {e}")


def check_and_alert():
    hostname, ip = get_hostname_ip()
    usage = get_disk_usage()
    alert = False
    alert_msg = f"*Disk Alert*\nHost: `{hostname}`\nIP: `{ip}`\n\n"
    for u in usage:
        if u['percent'] >= THRESHOLD:
            alert = True
            alert_msg += f"*{u['mountpoint']}*: {u['percent']}% used\n"
    if alert:
        send_telegram_alert(alert_msg)


def send_daily_report():
    hostname, ip = get_hostname_ip()
    usage = get_disk_usage()
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    report = f"*Disk Report*\nHost: `{hostname}`\nIP: `{ip}`\nTime: `{now}`\n\n"
    for u in usage:
        report += f"*{u['mountpoint']}*: {u['percent']}% used\n"
    send_telegram_alert(report)


if __name__ == "__main__":
    check_and_alert()
