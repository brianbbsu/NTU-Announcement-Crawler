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

class CN2019_AC_Pang_Crawler(BaseCrawler):

    _identifier = "Computer Networks 2019 (AC Pang)"
    url = "http://voip.csie.org/CN2019/"

    def _get_time_from_str(self, s):
        s = s[1:-1]
        date = dateutil.parser.parse(s)
        date = date.replace(tzinfo=gettz("Asia/Taipei"))
        return date

    def get_announcements(self):
        prog = re.compile(r"(\[\d\d\d\d\/\d\d\/\d\d\])")
        with requests.Session() as s:
            self.s = s
            r = s.get(self.url)
            anno_divs = bs4(r.text, "html.parser").find_all('p')
            arr = []
            for p in anno_divs:
                html_content = ''.join(str(x) for x in p.contents)
                result = prog.split(html_content)
                for x in result:
                    if prog.match(x):
                        arr.append([x,''])
                    elif len(arr):
                        arr[-1][1] += x
            annos = []
            it = 0
            arr = sorted(arr,reverse=True)
            for a in arr:
                title = ''.join(bs4(a[1], "html.parser").strings).strip()[:20]
                content = a[1]
                date = self._get_time_from_str(a[0])
                url = self.url
                classname = "Computer Networks 2019 (AC Pang)"
                anno = Announcement(title=title, content=content, date=date,
                                    url=url, pos=it, classname=classname)
                annos.append(anno)
                it += 1
        return annos


if __name__ == '__main__':
    c = CN2019Crawler()
    annos = c.get_announcements()
    print(annos)
