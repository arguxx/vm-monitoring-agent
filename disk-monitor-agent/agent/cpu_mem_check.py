import psutil
import socket
import requests
import os
from datetime import datetime
from config import BOT_TOKEN, CHAT_ID, THREAD_ID

CPU_THRESHOLD = int(os.getenv('CPU_THRESHOLD', 80))
MEM_THRESHOLD = int(os.getenv('MEM_THRESHOLD', 80))


def get_hostname_ip():
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except Exception:
        ip = 'Unknown'
    return hostname, ip


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_mem_usage():
    mem = psutil.virtual_memory()
    return mem.percent, mem.total, mem.used, mem.free


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
    cpu = get_cpu_usage()
    mem_percent, mem_total, mem_used, mem_free = get_mem_usage()
    alert = False
    alert_msg = f"*CPU/Mem Alert*\nHost: `{hostname}`\nIP: `{ip}`\n\n"
    if cpu >= CPU_THRESHOLD:
        alert = True
        alert_msg += f"*CPU*: {cpu}% used\n"
    if mem_percent >= MEM_THRESHOLD:
        alert = True
        alert_msg += f"*Memory*: {mem_percent}% used\n"
    if alert:
        send_telegram_alert(alert_msg)


def send_daily_report():
    hostname, ip = get_hostname_ip()
    cpu = get_cpu_usage()
    mem_percent, mem_total, mem_used, mem_free = get_mem_usage()
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    report = f"*CPU/Mem Report*\nHost: `{hostname}`\nIP: `{ip}`\nTime: `{now}`\n\n"
    report += f"*CPU*: {cpu}% used\n"
    report += f"*Memory*: {mem_percent}% used\n"
    send_telegram_alert(report)


if __name__ == "__main__":
    check_and_alert()
