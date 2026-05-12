import os
from dotenv import load_dotenv

# Load environment variables from /etc/disk-agent.env or .env
load_dotenv('/etc/disk-agent.env', override=True)
load_dotenv('.env', override=False)

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
THREAD_ID = os.getenv('THREAD_ID')
THRESHOLD = int(os.getenv('THRESHOLD', 80))
REPORT_TIME = os.getenv('REPORT_TIME', '07:00')

# Add more config as needed
