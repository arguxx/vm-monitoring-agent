# Customization Guide

This guide covers how to customize the VM Monitoring Agent to fit your needs.

## Environment Variables

All customization is done via the `/etc/disk-agent.env` file.

### Required Variables

```env
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
```

### Optional Variables

```env
THREAD_ID=123                    # Telegram topic/thread ID (optional)
THRESHOLD=80                     # Disk usage threshold percentage
CPU_THRESHOLD=80                 # CPU usage threshold percentage
MEM_THRESHOLD=80                 # Memory usage threshold percentage
REPORT_TIME=07:00                # Daily report time (HH:MM format)
```

## Threshold Configuration

### Disk Usage Threshold

Controls when disk alerts are sent:

```env
THRESHOLD=80
```

- **Default**: 80%
- **Range**: 0-100
- **Behavior**: Alert sent when any monitored mountpoint exceeds this percentage

### CPU Usage Threshold

Controls when CPU alerts are sent:

```env
CPU_THRESHOLD=80
```

- **Default**: 80%
- **Range**: 0-100
- **Behavior**: Alert sent when CPU usage exceeds this percentage

### Memory Usage Threshold

Controls when memory alerts are sent:

```env
MEM_THRESHOLD=80
```

- **Default**: 80%
- **Range**: 0-100
- **Behavior**: Alert sent when memory usage exceeds this percentage

### Example Thresholds

```env
# Strict monitoring (alert at 70%)
THRESHOLD=70
CPU_THRESHOLD=70
MEM_THRESHOLD=70

# Relaxed monitoring (alert at 90%)
THRESHOLD=90
CPU_THRESHOLD=90
MEM_THRESHOLD=90

# Different thresholds per metric
THRESHOLD=85          # Disk alert at 85%
CPU_THRESHOLD=75      # CPU alert at 75%
MEM_THRESHOLD=90      # Memory alert at 90%
```

## Schedule Configuration

### Using Systemd Timers

Edit the timer files in `/etc/systemd/system/`:

#### Disk Agent Timer

Edit `/etc/systemd/system/disk-agent.timer`:

```ini
[Timer]
OnBootSec=2min
OnUnitActiveSec=5min    # Change this to adjust interval
Unit=disk-agent.service
```

**Common intervals:**
- `OnUnitActiveSec=1min` - Every 1 minute
- `OnUnitActiveSec=5min` - Every 5 minutes (default)
- `OnUnitActiveSec=15min` - Every 15 minutes
- `OnUnitActiveSec=30min` - Every 30 minutes
- `OnUnitActiveSec=1h` - Every hour

#### CPU/Memory Agent Timer

Edit `/etc/systemd/system/cpu-mem-agent.timer`:

```ini
[Timer]
OnBootSec=2min
OnUnitActiveSec=5min    # Change this to adjust interval
Unit=cpu-mem-agent.service
```

#### Update Timer

Edit `/etc/systemd/system/disk-agent-update.timer`:

```ini
[Timer]
OnCalendar=*-*-* 06:00:00    # Change this to adjust update time
Unit=disk-agent-update.service
```

**Common schedules:**
- `OnCalendar=*-*-* 06:00:00` - Daily at 06:00 (default)
- `OnCalendar=*-*-* 00:00:00` - Daily at midnight
- `OnCalendar=hourly` - Every hour
- `OnCalendar=*-*-* 06:00,18:00:00` - Twice daily at 06:00 and 18:00

After editing, reload and restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart disk-agent.timer
sudo systemctl restart cpu-mem-agent.timer
sudo systemctl restart disk-agent-update.timer
```

### Using Cron

Edit crontab:

```bash
crontab -e
```

**Examples:**

```cron
# Every 1 minute
* * * * * /usr/bin/python3 /opt/disk-monitor-agent/agent/disk_check.py

# Every 5 minutes
*/5 * * * * /usr/bin/python3 /opt/disk-monitor-agent/agent/disk_check.py

# Every 15 minutes
*/15 * * * * /usr/bin/python3 /opt/disk-monitor-agent/agent/disk_check.py

# Every hour
0 * * * * /usr/bin/python3 /opt/disk-monitor-agent/agent/disk_check.py

# Every 6 hours
0 */6 * * * /usr/bin/python3 /opt/disk-monitor-agent/agent/disk_check.py

# Daily at 07:00
0 7 * * * /usr/bin/python3 /opt/disk-monitor-agent/agent/disk_check.py report
```

## Telegram Configuration

### Bot Token

Get your bot token from BotFather:

1. Open https://t.me/BotFather
2. Send `/newbot`
3. Follow instructions
4. Copy the token (e.g., `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

Set in `/etc/disk-agent.env`:

```env
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### Chat ID

Get your group/chat ID:

1. Add bot to your Telegram group
2. Send a message to the group
3. Run:

```bash
curl https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
```

4. Find the chat ID in the response (e.g., `-1001234567890`)

Set in `/etc/disk-agent.env`:

```env
CHAT_ID=-1001234567890
```

### Thread ID (Optional)

If using Telegram Topics/Threads:

1. Create a topic in your group
2. Send a message in that topic
3. Run the getUpdates command
4. Find the `message_thread_id` in the response

Set in `/etc/disk-agent.env`:

```env
THREAD_ID=123
```

### Disable Privacy Mode

Required for bot to read messages in groups:

1. Open BotFather
2. Send `/setprivacy`
3. Select your bot
4. Choose "Disable"

## Disk Monitoring Customization

### Exclude Mountpoints

Edit `agent/disk_check.py` to add more exclusions:

```python
exclude_mounts = ['/snap', '/var/lib/snapd', '/run', '/dev', '/sys', '/proc', '/your/custom/path']
```

### Exclude Filesystem Types

Edit `agent/disk_check.py`:

```python
exclude_fs = {'squashfs', 'tmpfs', 'devtmpfs', 'overlay', 'snap', 'nsfs', 'proc', 'sysfs', 'cgroup', 'fuse.lxcfs', 'your_fs_type'}
```

### Monitor Specific Mountpoints Only

Modify `get_disk_usage()` in `agent/disk_check.py`:

```python
def get_disk_usage():
    usage = []
    # Only monitor these mountpoints
    monitored_mounts = ['/', '/data', '/home']
    for part in psutil.disk_partitions():
        if part.mountpoint not in monitored_mounts:
            continue
        # ... rest of the code
```

## Alert Message Customization

### Modify Alert Format

Edit the message format in `agent/disk_check.py` or `agent/cpu_mem_check.py`:

**Disk Alert:**
```python
alert_msg = f"*Disk Alert*\nHost: `{hostname}`\nIP: `{ip}`\n\n"
# Add custom fields
alert_msg += f"Server: {hostname}\n"
alert_msg += f"Location: YourLocation\n"
```

**CPU/Memory Alert:**
```python
alert_msg = f"*CPU/Mem Alert*\nHost: `{hostname}`\nIP: `{ip}`\n\n"
# Add custom fields
alert_msg += f"Environment: Production\n"
```

### Add Custom Metadata

Add custom fields to the alert messages:

```python
def get_hostname_ip():
    hostname = socket.gethostname()
    ip = 'Unknown'
    # ... existing code ...
    
    # Add custom metadata
    environment = os.getenv('ENVIRONMENT', 'Unknown')
    location = os.getenv('LOCATION', 'Unknown')
    
    return hostname, ip, environment, location
```

Then use in alerts:
```python
hostname, ip, environment, location = get_hostname_ip()
alert_msg = f"*Disk Alert*\nHost: `{hostname}`\nIP: `{ip}`\nEnv: `{environment}`\nLocation: `{location}`\n\n"
```

## Service Path Configuration

If you installed the agent in a different location, update the systemd service files:

### Disk Agent Service

Edit `/etc/systemd/system/disk-agent.service`:

```ini
[Service]
Type=simple
EnvironmentFile=/etc/disk-agent.env
ExecStart=/usr/bin/python3 /your/custom/path/disk-monitor-agent/agent/disk_check.py
Restart=on-failure
```

### CPU/Memory Agent Service

Edit `/etc/systemd/system/cpu-mem-agent.service`:

```ini
[Service]
Type=simple
EnvironmentFile=/etc/disk-agent.env
ExecStart=/usr/bin/python3 /your/custom/path/disk-monitor-agent/agent/cpu_mem_check.py
Restart=on-failure
```

### Update Service

Edit `/etc/systemd/system/disk-agent-update.service`:

```ini
[Service]
Type=oneshot
ExecStart=/bin/bash /your/custom/path/disk-monitor-agent/scripts/update.sh
```

Then reload:

```bash
sudo systemctl daemon-reload
sudo systemctl restart disk-agent.timer cpu-mem-agent.timer
```

## Python Environment Customization

### Using Virtual Environment

If you prefer using a virtual environment:

1. Create venv:
```bash
cd /opt/disk-monitor-agent
python3 -m venv venv
source venv/bin/activate
pip install -r agent/requirements.txt
```

2. Update systemd services to use venv:

Edit `/etc/systemd/system/disk-agent.service`:
```ini
ExecStart=/opt/disk-monitor-agent/venv/bin/python agent/disk_check.py
```

Edit `/etc/systemd/system/cpu-mem-agent.service`:
```ini
ExecStart=/opt/disk-monitor-agent/venv/bin/python agent/cpu_mem_check.py
```

3. Reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart disk-agent.timer cpu-mem-agent.timer
```

### Using Different Python Version

If you need a specific Python version:

1. Install desired Python version
2. Update systemd service ExecStart to use that Python:
```ini
ExecStart=/usr/bin/python3.9 /opt/disk-monitor-agent/agent/disk_check.py
```

## Advanced Customization

### Add Custom Metrics

Add new monitoring metrics by creating new functions:

Example - Load Average:

```python
def get_load_average():
    load1, load5, load15 = os.getloadavg()
    return {
        '1min': load1,
        '5min': load5,
        '15min': load15
    }
```

Then integrate into `check_and_alert()` or `send_daily_report()`.

### Multiple Telegram Groups

Send alerts to multiple groups:

```python
def send_telegram_alert(message, chat_ids=None):
    if chat_ids is None:
        chat_ids = [CHAT_ID]
    
    for chat_id in chat_ids:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown',
        }
        if THREAD_ID:
            data['message_thread_id'] = THREAD_ID
        try:
            requests.post(url, data=data, timeout=10)
        except Exception as e:
            print(f"Failed to send alert to {chat_id}: {e}")
```

### Conditional Alerts

Only send alerts during certain hours:

```python
def should_send_alert():
    from datetime import datetime
    hour = datetime.now().hour
    # Only alert between 08:00 and 22:00
    return 8 <= hour <= 22

def check_and_alert():
    # ... existing code ...
    if alert and should_send_alert():
        send_telegram_alert(alert_msg)
```

### Alert Cooldown

Prevent alert spam by adding cooldown:

```python
import time
from datetime import datetime, timedelta

LAST_ALERT_TIME = {}
ALERT_COOLDOWN = 3600  # 1 hour in seconds

def check_and_alert():
    # ... existing code ...
    if alert:
        mountpoint_key = ','.join([u['mountpoint'] for u in usage if u['percent'] >= THRESHOLD])
        now = datetime.now()
        
        if mountpoint_key in LAST_ALERT_TIME:
            if (now - LAST_ALERT_TIME[mountpoint_key]).total_seconds() < ALERT_COOLDOWN:
                print("Alert cooldown active, skipping")
                return
        
        send_telegram_alert(alert_msg)
        LAST_ALERT_TIME[mountpoint_key] = now
```

## Testing Customizations

After making changes:

1. Test manually:
```bash
python3 agent/disk_check.py
python3 agent/cpu_mem_check.py
```

2. Check logs:
```bash
sudo journalctl -u disk-agent.service -f
sudo journalctl -u cpu-mem-agent.service -f
```

3. Restart services if needed:
```bash
sudo systemctl restart disk-agent.timer
sudo systemctl restart cpu-mem-agent.timer
```

## Configuration File Location

The agent looks for configuration in this order:

1. `/etc/disk-agent.env` (priority - override)
2. `.env` in the agent directory (fallback)

You can use both files - put sensitive data in `/etc/disk-agent.env` and defaults in `.env`.

## Example Complete Configuration

```env
# Telegram Configuration
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
CHAT_ID=-1001234567890
THREAD_ID=123

# Thresholds
THRESHOLD=85
CPU_THRESHOLD=75
MEM_THRESHOLD=90

# Report Schedule
REPORT_TIME=07:00

# Custom Metadata
ENVIRONMENT=Production
LOCATION=DataCenter-1
```

## Support

For issues or questions:
- Check logs: `sudo journalctl -u <service-name> -n 50`
- Verify environment variables: `cat /etc/disk-agent.env`
- Test scripts manually
- See [INSTALL.md](INSTALL.md) for installation help
