import threading
import time
import traceback

from crawl import crawl
from models import Announcement, PushRecord, Session
from utils import push_telegram_notification
import config


def process_notification():
    session = Session()
    tg_chat_id = config.get("telegram_chat_id")
    subq = session.query(PushRecord) \
        .filter_by(telegram_chat_id=tg_chat_id).subquery()
    new_announcements = session.query(Announcement).filter_by(present=True) \
        .outerjoin(subq, Announcement.id == subq.c.announcement_id) \
        .filter(subq.c.id == None).all()

    new_announcements = new_announcements[::-1]  # Push old announcemt first

    if not len(new_announcements):
        return

    print("Sending {} notification(s)...".format(len(new_announcements)))
    for anno in new_announcements:
        try:
            session = Session()
            push_telegram_notification(anno, tg_chat_id)
            session.add(PushRecord(announcement_id=anno.id,
                        telegram_chat_id=tg_chat_id))
            session.commit()
        except Exception:
            session.rollback()
    print("Done!")


def daemon_job(interval):
    """
        main function of the crawler daemon.
        interval: time in seconds between each crawl
    """
    time.sleep(3)  # Wait for api server to start first
    while True:
        try:
            crawl()
            process_notification()
        except Exception:
            traceback.print_exc()
        time.sleep(interval)


def start_daemon(interval=600):
    """
        Start crawler daemon in new thread.
        re-crawl every `interval` seconds
    """
    thread = threading.Thread(target=daemon_job, args=(interval, ))
    thread.daemon = True
    thread.start()
