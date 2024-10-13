import asyncio
import time
from radar_downloader import get_clouds_percentage
from credentials import *
import requests

def send_start_running():
    url_message = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

    for chat_id in CHAT_IDS:
        payload = {
            'chat_id': chat_id,
            'text': "Weather Radar Bot is running"
        }

        response = requests.post(url_message, data=payload)
        print(response.json())

def send_radar_report(message):

    url_message = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    url_photo = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto'

    for chat_id in CHAT_IDS:
        
        # Send text
        payload = {
            'chat_id': chat_id,
            'text': message
        }

        response = requests.post(url_message, data=payload)
        print(response.json())

        # Send radar image
        payload = {
            'chat_id': chat_id
        }
        file = {
            'photo': open("radar_tmp.jpg", 'rb')
        }

        response = requests.post(url_photo, data=payload, files=file)
        print(response.json())

async def check_radar_task():

    while(1):

        try:
            cloud_percentage = get_clouds_percentage(False)
            print(f"Percent =  {cloud_percentage}")

            if (cloud_percentage >= 5):
                delay_min = 15
                message = ""
                
                if cloud_percentage < 10:
                    message = f"There is some chance of rain: {cloud_percentage:.1f}%"
                    delay_min = 15
                    
                elif cloud_percentage > 10 and cloud_percentage < 20:
                    message = f"High chance of rain: {cloud_percentage:.1f}%"
                    delay_min = 30

                else :
                    message = f"It is probably raining now: {cloud_percentage:.1f}%"
                    delay_min = 90
            
                print("Sending message")
                send_radar_report(message)
                time.sleep(delay_min *60)
            
            else: 
                time.sleep(5*60)

        except Exception:
            time.sleep(60)
            
    # user_ids = ", ".join(str(uid) for uid in context.bot_data.setdefault("user_ids", set()))


async def main() -> None:
    send_start_running()
    await check_radar_task()


if __name__ == "__main__":
    asyncio.run(main())
