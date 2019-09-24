from .db import Base, Session, engine
from .announcement import Announcement

Base.metadata.create_all(engine)
