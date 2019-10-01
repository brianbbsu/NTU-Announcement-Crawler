from sqlalchemy import desc
import requests
import re
from models import Session, Announcement

import config

def escape_markdown_text(s):
    return re.sub(r"([_*`])", r"\\\1", s)

def get_submission_list():
    session = Session()
    return [ anno.dict() for anno in session.query(Announcement) \
                .filter_by(present=True).order_by(desc(Announcement.date), Announcement.pos).all()]

def push_telegram_notification(anno, chat_id):
    url = "https://api.telegram.org/bot{}/sendMessage".format(config.get("telegram_bot_token"))
    content = escape_markdown_text(anno.get_text_content())
    text = f"*{anno.classname} - {anno.title}*\n\n{content}\n\n"
    text += f"[Announcement Link]({anno.url})\n_Posted at: {anno.date_str()}_"
    r = requests.post(url, json = {
        "chat_id": chat_id,
        "parse_mode": "Markdown",
        "text": text
    })
