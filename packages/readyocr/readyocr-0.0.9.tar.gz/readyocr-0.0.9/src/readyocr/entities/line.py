from readyocr.entities.bbox import BoundingBox
from readyocr.entities.textbox import TextBox


class Line(TextBox):
    """
    To create a new :class:`Line` object we need the following

    :param id: Unique identifier of the Line entity.
    :type id: str
    :param bbox: Bounding box of the Line entity.
    :type bbox: BoundingBox
    :param text: Transcription of the Line object.
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