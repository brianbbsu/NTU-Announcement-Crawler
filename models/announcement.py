import datetime
import hashlib
from bs4 import BeautifulSoup as bs4

class Announcement(object):
    """
    Anno Structure
    {
      url: "Link to the anno or Link to the annos page",
      class_name: "Name of the class",
      crawler: "identifier of the crawler",
      date: "Announce Date of the anno",
      pos: "position within the class (smaller is newer, should be uniq, for sorting)",
      title: "Title of the anno",
      content: "Content of the anno" (in original html code)
    }
    """
    def date_str(self):
        return self.date.strftime("%Y-%m-%d")

    def get_raw_content(self):
        return self.content if self.content else "(empty)"

    def get_text_content(self):
        if not self.content:
            return "(empty)"
        else:
            return "\n".join(bs4(self.content, "html.parser").stripped_strings)

    def hash(self):
        # Consider crawler identifier, class_name, title, content, date
        s = self.crawler +  self.class_name + self.title + self.content + self.date_str()
        h = hashlib.sha1()
        h.update(s.encode("UTF-8"))
        return h.hexdigest()

    def basic_info(self):
        return f"{self.class_name} - title: {self.title} ({self.date_str()})"

    def __str__(self):
        date = self.date_str()
        content = self.get_text_content()
        return f"Announcement of {self.class_name} at {date} - {self.title}:\n\n{content}\n"

    def __init__(self, url=None, class_name="Undefined", \
                    date=datetime.date(1970, 1, 1), pos = 0, title = "", content="", crawler = None):
        self.url = url
        self.class_name = class_name
        self.date = date
        self.pos = pos
        self.title = title
        self.content = content
        self.crawler = None

