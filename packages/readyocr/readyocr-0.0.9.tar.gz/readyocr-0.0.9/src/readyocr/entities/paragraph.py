from readyocr.entities.bbox import BoundingBox
from readyocr.entities.textbox import TextBox


class Paragraph(TextBox):
    """
    To create a new :class:`Paragraph` object we need the following

    :param id: Unique identifier of the Paragraph entity.
    :type id: str
    :param bbox: Bounding box of the Paragraph entity.
    :type bbox: BoundingBox
    :param text: Transcription of the Paragraph object.
    :type text: str
    :param confidence: value storing the confidence of detection out of 100.
    :type confidence: float
    """

    def __init__(
        self,
        id: str,
        bbox: BoundingBox,
        text: str="",
        confidence: float=0
    ):
        super().__init__(id, bbox, text, confidence)

    def __repr__(self):
        return f"Paragraph(id: '{self.id}', x: {self.bbox.x}, y: {self.bbox.y}, width: {self.bbox.width}, height: {self.bbox.height}, text: {self.text},confidence: {self.confidence}, tags: [{self._tags}])"