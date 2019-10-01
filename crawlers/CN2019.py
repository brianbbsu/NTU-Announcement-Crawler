import requests
from bs4 import BeautifulSoup as bs4
import re
import datetime
import dateutil.parser
from dateutil.tz import gettz
import json

from models import Announcement
import config
from . import BaseCrawler


class CN2019Crawler(BaseCrawler):

    _identifier = "Computer Networks 2019"
    url = \
        "http://www.cmlab.csie.ntu.edu.tw/~chenyuyang/CN2019/announcement.html"

    def _get_time_from_post(self, p):
        month = p.find(class_="month").string
        day = p.find(class_="day").string
        date = dateutil.parser.parse(month + " " + day)
        date = date.replace(tzinfo=gettz("Asia/Taipei"))
        if date.month >= 9:
            date = date.replace(year=2019)
        else:
            date = date.replace(year=2020)
        return date

    def get_announcements(self):
        with requests.Session() as s:
            self.s = s
            r = s.get(self.url)
            anno_divs = bs4(r.text, "html.parser").findAll(class_="post")
            annos = []
            it = 0
            for p in anno_divs:
                title = "\n".join(p.find(class_="title").stripped_strings)
                content = p.find(class_="title").next_sibling.strip()
                date = self._get_time_from_post(p)
                url = self.url
                classname = "Computer Networks 2019"
                anno = Announcement(title=title, content=content, date=date,
                                    url=url, pos=it, classname=classname)
                annos.append(anno)
                it += 1
        return annos


if __name__ == '__main__':
    c = CN2019Crawler()
    annos = c.get_announcements()
    print(annos)
