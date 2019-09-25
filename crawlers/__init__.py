from .base import BaseCrawler

from .NTU_ceiba import CeibaCrawler
from .NTU_cool import NTUCoolCrawler
from .CN2019 import CN2019Crawler

crawler_list = [CeibaCrawler, NTUCoolCrawler, CN2019Crawler]
