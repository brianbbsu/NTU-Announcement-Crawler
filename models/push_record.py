from . import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func


class PushRecord(Base):
    __tablename__ = "push_records"

    # pk of the record in the DB
    id = Column(Integer, primary_key=True)

    # announcement id of this record
    announcement_id = Column(Integer, ForeignKey('announcements.id'),
                             nullable=False)

    # telegram chat id of the receiver
    telegram_chat_id = Column(String, nullable=False)

    # push date time
    date = Column(DateTime, server_default=func.now())
