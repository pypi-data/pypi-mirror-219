import os
from readyocr.entities.bbox import SpatialObject
from readyocr.entities.entity_list import EntityList
from readyocr.entities.page_entity import PageEntity


class Page(SpatialObject):
    """ 
    Creates a new document, ideally representing a single item in the dataset.
    
    :param id: Unique id of the Page
    :type id: str
    :param width: Width of page, in pixels
    :type width: float
    :param height: Height of page, in pixels
    :type height: float
    :param page_num: Page number in the document linked to this Page object
    :type page_num: int
    :param children: Child entities in the Page
    :type children: List
    """

    def __init__(
        self,
        id: str,
        width: int,
        height: int,
        page_num: int=-1,
        image=None
    ):
        super().__init__(width=width, height=height)
        self.id = id
        self.metadata = {}
        self.page_num = page_num
        self.image = image
        self._children = EntityList()

    @property
    def children(self) -> EntityList:
        """
        :return: Returns all the objects present in the Page.
        :rtype: EntityList
        """
        return self._children
    
    # @children.setter
    # def children(self, children):
    #     """
    #     :param children: List of children entities.
    #     :type children: list
    #     """
    #     self._children = EntityList(children)
    #     for desc in self.descendants:
    #         desc.page_num = self.page_num
    #         desc.page_id = self.id

    def add(self, child: PageEntity):
        """
        _summary_

        :return: _description_
        :rtype: _type_
        """
        self._children.add(child)

    @property
    def descendants(self):
        """
        :return: Returns all the children of the entity.
        :rtype: list
        """
        descendants = []
        for x in self.children:
            if len(x.descendants) > 0:
                descendants.extend(x.descendants)
        descendants.extend(self.children)
        # remove mutual descendants
        descendants = list(set(descendants))
        return EntityList(descendants)
    
    def find_parent_by_child_id(self, child_id: str) -> EntityList:
        """
        Find the parent of a child entity by its ID.

        :param child_id: ID of the child entity.
        :type child_id: str
        :return: Returns the parent entity of the child entity.
        :rtype: EntityList
        """
        parents = []
        for desc in self.descendants:
            child_ids = [x.id for x in desc.children]
            if child_id in child_ids:
                parents.append(desc)
        # remove mutual parents
        parents = list(set(parents))
        return EntityList(parents)
    
    def __repr__(self):
        return os.linesep.join([
            f"Page(id: {self.id}, width: {self.width}, height: {self.height}, page_num: {self.page_num})",
            f"Children - {len(self.children)}"
        ])
    
    def export_json(self):
        return {
            "id": self.id,
            "pageNumber": self.page_num,
            "dimension": {
                "width": self.width,
                "height": self.height
            },
            "entities": [x.export_json() for x in self.descendants]
        }
