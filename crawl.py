#!/usr/bin/env python3
from models import Announcement, Base, Session
from crawlers import crawler_list

def get_announcements():
    """
        Get all announcements using crawlers listed in crawlers/__init__.py
    """
    annos = []
    for crawler_cls in crawler_list:
        c = crawler_cls()
        print("Getting announcement from {}...".format(c.identifier))
        new_annos = c.get_announcements()
        for anno in new_annos:
            anno.crawler = c.identifier
        print("Got {} annoumcement(s) from {}.".format(len(new_annos), c.identifier))
        annos += new_annos
    return annos

def update_database(annos):
    """
        Update database with new list of announcements.
        Old annoucements will be marked as "not present"
    """
    print("Updating Database...")
    session = Session()
    try:
        session.query(Announcement).filter_by(present=True).update({"present": False})
        for anno in annos:
            anno.save(session)
        session.commit()
    except:
        print("Failed!")
        session.rollback()
        raise
    finally:
        print("Done!")
        session.close()

def crawl():
    """
        Crawl announcements and update database
    """
    annos = get_announcements()
    print("Total: {} announcement(s)".format(len(annos)))
    update_database(annos)

if __name__ == "__main__":
    crawl()
