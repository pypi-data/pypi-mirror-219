import os
from typing import TypeVar, Generic
from typing_extensions import Self


T = TypeVar('T')


class EntityList(set, Generic[T]):
    """
    Creates a list type object, initially empty but extended with the list passed in objs.

    :param obj: Custom list of objects.
    :type objs: list
    """

    def __init__(self, objs=None):
        super().__init__()
        
        if objs is None:
            objs = set()
        elif isinstance(objs, list):
            objs = set(objs)
        elif not isinstance(objs, set):
            objs = set([objs])

        self.update(objs)

    def filter_by_class(self, type) -> Self:
        """
        Filters the list of entities by class type.

        :param type: Class type to filter by.
        :type type: class
        :return: Returns a list of entities filtered by class type.
        :rtype: EntityList
        """
        filtered = []
        for x in self:
            if isinstance(x, type):
                filtered.append(x)
        return EntityList(filtered)
    
    def filter_by_attr(self, attr, value) -> Self:
        """
        Filters the list of entities by attribute value.

        :param attr: Attribute to filter by.
        :type attr: str
        :param value: Value to filter by.
        :type value: Any
        :return: Returns a list of entities filtered by attribute value.
        :rtype: EntityList
        """
        filtered = []
        for x in self:
            if hasattr(x, attr) and getattr(x, attr) == value:
                filtered.append(x)
        return EntityList(filtered)
    
    def filter_by_tags(self, tags) -> Self:
        """
        Filters the list of entities by tags.

        :param tags: List of tags to filter by.
        :type tags: list or str
        :return: Returns a list of entities filtered by tags.
        :rtype: EntityList
        """
        filtered = []
        for x in self:
            if x.tags.has(tags):
                filtered.append(x)

        return EntityList(filtered)
    
    def get_all_tags(self) -> set:
        """
        Gets a list of all tags.

        :return: Returns a list of all tags.
        :rtype: list
        """
        tags = []
        for x in self:
            tags.extend(x.tags)
        return set(tags)
    
    def get_ids(self) -> list:
        """
        Gets a list of ids from the list of entities.

        :return: Returns a list of ids.
        :rtype: list
        """
        return [x.id for x in self]
    
    def get_by_id(self, id) -> T:
        """
        Gets an entity by id.

        :param id: Id of entity to get.
        :type id: str
        :return: Returns an entity.
        :rtype: Entity
        """
        for x in self:
            if x.id == id:
                return x
        return None
    
    def __repr__(self) -> str:
        return os.linesep.join([str(x) for x in self])