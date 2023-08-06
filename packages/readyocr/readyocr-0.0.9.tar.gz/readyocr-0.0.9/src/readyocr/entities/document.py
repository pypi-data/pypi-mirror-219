import os
from typing import List

from readyocr.entities.bbox import SpatialObject
from readyocr.entities.page import Page
from readyocr.entities.entity_list import EntityList
from readyocr.exceptions import InputError


class Document(SpatialObject):
    """ 
    Represents the description of a single document, as it would appear in the input to the Textract API.
    Documnent serves as the root node of the object model hierarchy,
    which should be used as an intermediate form for most analytic purposes.
    The Document node also contains the metadata of the document.
    """

    def __init__(self, num_pages: int = 1):
        """ 
        Creates a new document, ideally containing entity objects pertaining to each page.

        :param num_pages: Number of pages in the input Document.
        """
        super().__init__(width=0, height=0)
        self.num_pages: int = num_pages
        self._pages: List[Page] = []
        self.response = None

    @property
    def pages(self) -> List[Page]:
        """
        Returns all the :class:`Page` objects present in the Document.

        :return: List of Page objects, each representing a Page within the Document.
        :rtype: List
        """
        return self._pages
    
    @pages.setter
    def pages(self, pages: List[Page]):
        """
        Add Page objects to the Document.

        :param pages: List of Page objects, each representing a Page within the Document. No specific ordering is assumed with input.
        :type pages: List[Page]
        """
        self._pages = sorted(pages, key=lambda x: x.page_num)

    def add(self, page: Page):
        """
        Add Page object to the Document.

        :param page: Page object to be added to the Document.
        :type page: Page
        """
        self.pages.append(page)

    def page(self, page_no: int = 0):
        """
        Returns :class:`Page` object/s depending on the input page_no. Follows zero-indexing.

        :param page_no: if int, returns single Page Object, else if list, it return a list of Page objects.
        :type page_no: int if single page, list of int if multiple pages

        :return: Filters and returns Page objects depending on the input page_no
        :rtype: Page or List[Page]
        """
        if isinstance(page_no, int):
            return self.pages[page_no]
        elif isinstance(page_no, list):
            return [self.pages[num] for num in page_no]
        else:
            raise InputError("page_no parameter doesn't match required data types.")
    
    @property
    def descendants(self) -> EntityList:
        """ 
        :return: Returns all the objects present in the Document.
        :rtype: EntityList
        """
        descendants = []
        for page in self.pages:
            descendants.extend(page.descendants)

        return EntityList(descendants)
    
    def __repr__(self):
        return os.linesep.join([
            "This document holds the following data:",
            f"Pages - {len(self.pages)}",
            f"Descendants - {len(self.descendants)}"
        ])
    
    def export_json(self):
        return {
            "document": {
                "pages": [
                    page.export_json() for page in self._pages
                ]
            }
        }