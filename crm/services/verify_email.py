from email.message import EmailMessage
from pathlib import Path
import aiosmtplib

from config import settings, EMAIL_USE_SSL

async def send_verification_email(email_to: str, verification_url: str):
    # Чтение шаблона
    template_path = Path(__file__).parent.parent / "templates" / "verify_email.html"
    with open(template_path, "r") as f:
        html_content = f.read().replace("{{ verification_url }}", verification_url)
    
    # Создание сообщения
    message = EmailMessage()
    message["From"] = f"Test <{settings.EMAIL_HOST_USER}>"
    message["To"] = email_to
    message["Subject"] = "Подтвердите ваш email"
    message.set_content(html_content, subtype="html")
    
    # Отправка
    await aiosmtplib.send(
        message,
        hostname=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=EMAIL_USE_SSL,
    )
