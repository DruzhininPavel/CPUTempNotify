from flask import Flask
from gpiozero import CPUTemperature
import requests
import time
import threading

# Initialize Flask application
app = Flask(__name__)

# Replace these with your Telegram bot's token and the chat ID
TELEGRAM_TOKEN = 'your_bot_token'
CHAT_ID = 'your_chat_id'

# URL for the Telegram API
TELEGRAM_SEND_MESSAGE_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'


# Function to send a message to Telegram
def send_telegram_message(msg):
    data = {
        'chat_id': CHAT_ID,
        'text': msg,
    }
    response = requests.post(TELEGRAM_SEND_MESSAGE_URL, data=data)
    return response.json()


# Function to monitor the CPU temperature
def monitor_cpu_temp():
    cpu = CPUTemperature()
    while True:
        temp = cpu.temperature
        if temp >= 50.0:
            send_telegram_message(f'Warning! CPU Temperature is high: {temp}°C')
        time.sleep(60)  # Check every 60 seconds


# Start the monitoring in a background thread
def start_monitoring():
    thread = threading.Thread(target=monitor_cpu_temp)
    thread.start()


@app.route('/')
def index():
    return 'CPU Temperature Monitor is running!'


def main():
    start_monitoring()
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
