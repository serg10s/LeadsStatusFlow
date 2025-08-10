import aiohttp
from config import settings
import json

test_data = {'first_name': 'admin', 'last_name': 'admin', 'email': 'quappomozisei-7352@yopmail.com', 'password': '$2b$12$GlnFRqgzSdbv6/EkGC9dguGUJE/0X86TAPlua0NLDoojpfrIKUdDq'}


def creating_text(data: dict):
    return f"Full name: {data['last_name']} {data['first_name']}\nEmail: {data['email']}"
    

async def sendig_admins_for_verification(url: str, chat_id: str, text: str, keyboard=None):
    async with aiohttp.ClientSession() as session:
        sending_data = {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": None,
            "reply_to_message_id": None
        }
        if keyboard:
            sending_data['reply_markup'] = keyboard
            await session.post(url=url, json=sending_data)
            await session.close()
        else:
            await session.post(url=url, json=sending_data)
            await session.close()           


async def push_telegram_admin(data: dict, chat_id: str = '-4778572047'):
    website = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage"
    keyboard = json.dumps({
            "inline_keyboard": [
                [
                    {
                        "text": 'Approve',
                        'callback_data': 'approve'
                        },
                    {
                        "text": "Reject",
                        'callback_data': 'reject'
                    },
                ]
                                ]
            })

    return await sendig_admins_for_verification(
            url=website, 
            text=creating_text(data),
            chat_id=chat_id,
            keyboard=keyboard
     )   


async def delete_admin():
    ...
