#!/usr/bin/env python3
import config

annos = []

for crawler_cls in config.crawler_list:
    c = crawler_cls()
    print("Getting announcement from {}...".format(c.identifier))
    new_annos = c.get_announcements()
    for anno in new_annos:
        anno.crawler = c.identifier
    print("Got {} annoumcement(s) from {}.".format(len(new_annos), c.identifier))
    annos += new_annos
annos = sorted(annos, key=lambda x:(x.date, -x.pos))

for anno in annos:
    print(anno.basic_info())

