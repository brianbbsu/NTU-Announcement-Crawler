from sqlalchemy import desc
from models import Session, Announcement

def get_submission_list():
    session = Session()
    return [ anno.dict() for anno in session.query(Announcement) \
                .filter_by(present=True).order_by(desc(Announcement.date), Announcement.pos).all()]

