from .base import BaseCrawler

from .ceiba import CeibaCrawler
from .cool import NTUCoolCrawler
from .CN2019 import CN2019Crawler

crawler_list = [CeibaCrawler, NTUCoolCrawler, CN2019Crawler]
