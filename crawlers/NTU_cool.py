import requests
from bs4 import BeautifulSoup as bs4
import re
import datetime
import dateutil.parser
import json

from models import Announcement
import config
from . import BaseCrawler

class NTUCoolCrawler(BaseCrawler):
    
    _identifier = "NTU Cool"

    def _get_announcements_from_class_id(self, s, cid):
        r = s.get(f"https://cool.ntu.edu.tw/api/v1/courses/{cid}/discussion_topics?only_announcements=true&per_page=100000")
        dt = json.loads(r.text[9:])
        annos = []
        it = 0
        for anno in dt:
            content = anno["message"]
            annos.append(Announcement(url = anno["url"], date = dateutil.parser.parse(anno["posted_at"]), pos = it, title = anno["title"], content = content))
            it += 1
        return annos

    def _login(self, s):
        pre_login_req = s.get("https://cool.ntu.edu.tw/login/saml")
        form1 = bs4(pre_login_req.text, "html.parser").find("form")
        data1 = {}
        for inp in form1.findAll("input"):
            data1[inp.get("name")] = inp.get("value") or ""
        data1["ctl00$ContentPlaceHolder1$UsernameTextBox"] = config.ntu_user
        data1["ctl00$ContentPlaceHolder1$PasswordTextBox"] = config.ntu_pass
        login_req = s.post("https://adfs.ntu.edu.tw/" + form1.get("action"), data = data1, allow_redirects=True)
        form2 = bs4(login_req.text, "html.parser").find("form")
        data2 = {}
        for inp in form2.findAll("input"):
            data2[inp.get("name")] = inp.get("value") or ""
        post_login_req = s.post(form2.get("action"), data = data2, allow_redirects=True) 

    def _get_courses(self, s):
        r = s.get("https://cool.ntu.edu.tw/api/v1/courses")
        return json.loads(r.text[9:])

    def get_announcements(self):
        with requests.Session() as s:
            self._login(s)
            courses = self._get_courses(s)
            annos = []
            for c in courses:
                course_annos = self._get_announcements_from_class_id(s, c["id"])
                for anno in course_annos:
                    anno.classname = c["name"]
                annos += course_annos
        return annos

if __name__ == '__main__':
    c = NTUCoolCrawler()
    annos = c.get_announcements()
    print(annos)
