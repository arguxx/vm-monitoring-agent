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
    ip = 'Unknown'
    # Try to get the main non-localhost IP
    try:
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                    ip = addr.address
                    break
            if ip != 'Unknown':
                break
    except Exception:
        pass
    return hostname, ip



def get_cpu_usage():
    return psutil.cpu_percent(interval=1)



def get_mem_usage():
    mem = psutil.virtual_memory()
    return {
        'percent': mem.percent,
        'total': mem.total,
        'used': mem.used,
        'free': mem.free
    }

def format_bytes(size):
    # Human-readable memory size
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


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
    mem = get_mem_usage()
    alert = False
    alert_msg = f"*CPU/Mem Alert*\nHost: `{hostname}`\nIP: `{ip}`\n\n"
    if cpu >= CPU_THRESHOLD:
        alert = True
    if mem['percent'] >= MEM_THRESHOLD:
        alert = True
    if alert:
        alert_msg += f"*CPU*: {cpu}% used\n"
        alert_msg += f"*Memory*: {mem['percent']}% used\n"
        alert_msg += f"Total: {format_bytes(mem['total'])}, Used: {format_bytes(mem['used'])}, Free: {format_bytes(mem['free'])}\n"
        send_telegram_alert(alert_msg)



def send_daily_report():
    hostname, ip = get_hostname_ip()
    cpu = get_cpu_usage()
    mem = get_mem_usage()
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    report = f"*CPU/Mem Report*\nHost: `{hostname}`\nIP: `{ip}`\nTime: `{now}`\n\n"
    report += f"*CPU*: {cpu}% used\n"
    report += f"*Memory*: {mem['percent']}% used\n"
    report += f"Total: {format_bytes(mem['total'])}, Used: {format_bytes(mem['used'])}, Free: {format_bytes(mem['free'])}\n"
    send_telegram_alert(report)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        send_daily_report()
    else:
        check_and_alert()


if __name__ == "__main__":
    check_and_alert()
