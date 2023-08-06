from readyocr.entities.bbox import BoundingBox
from readyocr.entities.page_entity import PageEntity


class Table(PageEntity):
    """
    To create a new :class:`Table` object we need the following

    :param id: Unique identifier of the Table entity.
    :type id: str
    :param bbox: Bounding box of the Table entity.
    :type bbox: BoundingBox
    :param confidence: value storing the confidence of detection out of 100.
    :type confidence: float
    """

    def __init__(
        self,
        id: str,
        bbox: BoundingBox,
        confidence: float=0,
        title: str=''
    ):
        super().__init__(id, bbox)
        self.confidence = confidence
        self._title = title

    @property
    def title(self) -> str:
        """
        :return: Returns the title of the Table
        :rtype: str
        """
        return self._title
    
    @title.setter
    def title(self, title: str):
        """
        Sets the title of the Table

        :param title: title of the Table
        :type title: str
        """
        self._title = title

    def add(self, child: PageEntity):
        """
        _summary_

        :return: _description_
        :rtype: _type_
        """
        self._children.add(child)