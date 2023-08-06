"""
:class:`PageEntity` is the class that all Document entities such as :class:`Word`, :class:`Line`,
:class:`Table` etc. inherit from. This class provides methods useful to all such entities.
"""
from abc import ABC
from typing import Dict
from typing_extensions import Self

from readyocr.entities.bbox import BoundingBox
from readyocr.entities.entity_list import EntityList
from readyocr.entities.entity_tag import EntityTag


class PageEntity(ABC):
    """
    :param id: Unique identifier for the document entity.

    :param ABC: Abstract Base Class for all Document entities.
    :type ABC: ABC
    """

    def __init__(self, entity_id: str, bbox: BoundingBox):
        """
        Initialize the common properties to DocumentEntities. Additionally, it contains
        information about the child entities within a document entity.

        :param entity_id: Unique identifier for the document entity.
        :param bbox: Bounding box of the entity
        """

        self.id = entity_id
        self._bbox: BoundingBox = bbox
        self.metadata = dict() # Holds optional information about the entity
        self._children = EntityList()
        self._raw_object = None
        self._tags = EntityTag()

    @property
    def raw_object(self) -> Dict:
        """
        :return: Returns the raw dictionary object that was used to create this Python object
        :rtype: Dict
        """
        return self._raw_object
    
    @raw_object.setter
    def raw_object(self, raw_object: Dict):
        """
        Set the raw object that was used to create this Python object,
        :param raw_object: raw object dictionary from the response
        :type raw_object: Dict
        """
        self._raw_object = raw_object

    @property
    def x(self) -> float:
        """
        :return: Returns x coordinate for bounding box
        :rtype: float
        """
        return self._bbox.x
    
    @x.setter
    def x(self, x: float):
        """
        Sets x coordinate for bounding box

        :param x: x coordinate of the bounding box
        :type x: float
        """
        self._bbox.x = x
    
    @property
    def y(self) -> float:
        """
        :return: Returns y coordinate for bounding box
        :rtype: float
        """
        return self._bbox.y
    
    @y.setter
    def y(self, y: float):
        """
        Sets y coordinate for bounding box.

        :param y: y coordinate of the bounding box
        :type y: float
        """
        self._bbox.y = y
    
    @property
    def width(self) -> float:
        """
        :return: Returns width of bounding box
        :rtype: float
        """
        return self._bbox.width
    
    @width.setter
    def width(self, width: float):
        """
        Sets width for bounding box.

        :param width: width of the bounding box
        :type width: float
        """
        self._bbox.width = width
    
    @property
    def height(self) -> float:
        """
        :return: Returns height of bounding box
        :rtype: float
        """
        return self._bbox.height
    
    @height.setter
    def height(self, height: float):
        """
        Sets height for bounding box.
        
        :param height: height of the bounding box
        :type height: float
        """
        self._bbox.height = height

    @property
    def bbox(self) -> BoundingBox:
        """
        :return: Returns entire bounding box of entity
        :rtype: BoundingBox
        """
        return self._bbox
    
    @property
    def children(self) -> EntityList[Self]:
        """
        :return: Returns all the objects present in the Page.
        :rtype: EntityList
        """
        return self._children
    
    @property
    def tags(self) -> EntityTag:
        """
        :return: Returns all the tags of this entity.
        :rtype: EntityTag
        """
        return self._tags

    @property
    def descendants(self) -> EntityList[Self]:
        """
        :return: Returns all the children of the entity.
        :rtype: EntityList
        """
        descendants = set()
        for child in self.children:
            descendants.add(child)
            for desc in child.descendants:
                if desc not in descendants:
                    descendants.add(desc)

        descendants = list(descendants)
        
        return EntityList(descendants)
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id: '{self.id}', confidence: {self.confidence}, tags: [{self._tags}])"
    
    def __eq__(self, other):
        if isinstance(other, PageEntity):
            return self.id == other.id
        return NotImplemented
    
    def __hash__(self):
        return hash(self.id)

    def export_json(self):
        """
        Exports the entity as a JSON object.
        """
        return {
            "id": self.id,
            "class": self.__class__.__name__,
            "boundingBox": self.bbox.export_json(),
            "metadata": self.metadata,
            "tags": [tag for tag in self.tags],
            "childrenIds": [child.id for child in self.children]
        }