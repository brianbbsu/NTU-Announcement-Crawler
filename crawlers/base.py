import abc

class BaseCrawler(abc.ABC):
    """
        Base class for a crawler
    """
    @property
    def identifier(self):
        """
            return the identifier of this crawler
        """
        if not hasattr(self, "_identifier"):
            raise Exception("The crawler implemtation didn't set the _identifier var.")
        return self._identifier

    @abc.abstractmethod
    def get_announcements(self):
        """
            return an array of Announcement object, represents annoumcements got from this crawler.
        """
        raise NotImplementedError
