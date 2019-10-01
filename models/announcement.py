import datetime
import hashlib
from bs4 import BeautifulSoup as bs4

from . import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, desc

class Announcement(Base):
    """
    Anno Structure
    {
      url: "Link to the anno or Link to the annos page",
      classname: "Name of the class",
      crawler: "identifier of the crawler",
      date: "Announce Date of the anno",
      pos: "position within the class (smaller is newer, should be uniq, for sorting)",
      title: "Title of the anno",
      content: "Content of the anno" (in original html code),
    }
    """
    __tablename__ = "announcements"

    # pk of the anno in the DB
    id = Column(Integer, primary_key = True)

    # digest of the anno, calculated with self.hash()
    digest = Column(String, unique = True, nullable = False)

    # URL to the anno or annos page
    url = Column(String)

    # Crawler identifier
    crawler = Column(String, nullable = False)

    # Class Name
    classname = Column(String, nullable = False)

    # Title of the anno
    title = Column(String, nullable = False)

    # Content in raw html of the anno
    content = Column(String, nullable = False)

    # Announce date of the anno
    date = Column(DateTime, nullable = False)

    # position of the anno relative to other annos from the same (crawler, classname)
    # Smaller is newer
    pos = Column(Integer, nullable = False)

    # Present?
    present = Column(Boolean, nullable = False, default = True)

    __mapper_args__ = {
        "order_by": (desc(date), pos)
    }

    def date_str(self):
        return self.date.strftime("%Y-%m-%d")

    def get_text_content(self):
        ret = "" if self.content is None \
                else "\n".join(bs4(self.content, "html.parser").stripped_strings)
        if ret == "":
            return "(Empty announcement.)"
        else:
            return ret

    def hash(self):
        # Consider crawler identifier, classname, title, content, date
        s = self.crawler +  self.classname + self.title + self.content + self.date_str()
        h = hashlib.sha1()
        h.update(s.encode("UTF-8"))
        return h.hexdigest()

    def basic_info(self):
        return f"{self.classname} - title: {self.title} ({self.date_str()})"

    def __str__(self):
        date = self.date_str()
        content = self.get_text_content()
        return f"Announcement of {self.classname} at {date} - {self.title}:\n\n{content}\n"

    def dict(self):
        ret = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        ret["text_content"] = self.get_text_content()
        return ret

    def save(self, session):
        self.digest = self.hash()
        anno = session.query(Announcement).filter_by(digest = self.digest).first()
        if anno:
            # Update fields not used for calculation of digest
            anno.present = True
            anno.url = self.url
            anno.pos = self.pos
        else:
            anno = self
        session.add(anno)
