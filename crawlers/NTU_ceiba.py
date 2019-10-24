import requests
from bs4 import BeautifulSoup as bs4
import re
import datetime
import dateutil.parser
from dateutil.tz import gettz

from models import Announcement
import config
from . import BaseCrawler


class CeibaCrawler(BaseCrawler):

    _identifier = "NTU Ceiba"
    base_url = "https://ceiba.ntu.edu.tw/"

    def _get_class_id_from_url(self, url):
        r = self.s.get(url, allow_redirects=True)
        mat = re.search(r"course\/([^/]+)\/", r.url)
        if mat is not None:
            return mat.group(1)
        else:
            return None

    def _get_announcement_from_url(self, url):
        req = self.s.get(url)
        req.encoding = "UTF-8"
        table = bs4(req.text, "html.parser").find("table")
        rows = table.find_all("tr")
        title = rows[0].find("td").string
        content = str(rows[5].find("td"))
        date = dateutil.parser.parse(rows[1].find("td").string)
        date = date.replace(tzinfo=gettz("Asia/Taipei"))
        return Announcement(title=title, content=content, url=url, date=date)

    def _get_announcements_from_class_id(self, class_id):
        test_req = self.s.get(self.base_url
                              + (f"modules/bulletin/bulletin.php"
                                 f"?default_lang=chinese&csn={class_id}"))
        test_req.encoding = "UTF-8"
        if len(test_req.text) < 100:
            return None
        annos = []
        it = 0
        while True:
            url = self.base_url \
                + "modules/bulletin/bulletin.php?startrec=" + str(it)
            req = self.s.get(url)
            req.encoding = "UTF-8"
            table = bs4(req.text, "html.parser").find("table")
            rows = table.find_all("tr")[1:]
            if len(rows) == 0:
                break
            for r in rows:
                orig_url = r.find_all("td")[2].find("a").get("href")
                sn = re.search(r"sn=(\d+)", orig_url).group(1)
                url = self.base_url \
                    + (f"modules/bulletin/bulletin_popup.php"
                       f"?current_lang=chinese&sn={sn}&csn={class_id}")
                anno = self._get_announcement_from_url(url)
                anno.pos = len(annos) + 1
                annos.append(anno)
            it += 10
        return annos

    def _login(self):
        pre_login_req = \
            self.s.get(("https://web2.cc.ntu.edu.tw/p/s/login2/p6.php?"
                        "url=https://ceiba.ntu.edu.tw/ChkSessLib.php"),
                       allow_redirects=True)
        login_req = self.s.post("https://web2.cc.ntu.edu.tw/p/s/login2/p1.php",
                                data={
                                    "user": config.get("ntu_user"),
                                    "pass": config.get("ntu_pass")
                                }, allow_redirects=True)
        post_login_req = self.s.get("https://ceiba.ntu.edu.tw/ChkSessLib.php",
                                    allow_redirects=True)
        if post_login_req.url != "https://ceiba.ntu.edu.tw/student/index.php":
            print("Login Failed!")
            exit(1)

    def get_announcements(self):
        annos = []
        with requests.Session() as s:
            self.s = s
            self._login()
            class_table_req = self.s.get(self.base_url + "student/index.php")
            class_table_req.encoding = "UTF-8"
            class_table = bs4(class_table_req.text, "html.parser").\
                find("table").find_all("tr")[1:]

            for cls in class_table:
                classname_cell = cls.find_all("td")[4].find("a")
                classname = classname_cell.string
                class_url = classname_cell.get('href')
                class_id = self._get_class_id_from_url(class_url)
                class_annos = self._get_announcements_from_class_id(class_id)
                if class_annos:
                    for anno in class_annos:
                        anno.classname = classname
                    annos += class_annos
        return annos


if __name__ == '__main__':
    c = CeibaCrawler()
    annos = c.get_announcements()
    print(annos)
