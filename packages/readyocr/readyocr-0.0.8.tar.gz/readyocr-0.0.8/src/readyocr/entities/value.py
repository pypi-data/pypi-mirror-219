from readyocr.entities.bbox import BoundingBox
from readyocr.entities.textbox import TextBox


class Value(TextBox):
    """
    To create a new :class:`Value` object we need the following

    :param id: Unique identifier of the Value entity.
    :type id: str
    :param bbox: Bounding box of the Value entity.
    :type bbox: BoundingBox
    :param text: Transcription of the Value object.
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