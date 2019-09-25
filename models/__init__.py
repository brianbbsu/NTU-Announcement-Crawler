from .db import Base, Session, engine
from .announcement import Announcement
from .push_record import PushRecord

Base.metadata.create_all(engine)
