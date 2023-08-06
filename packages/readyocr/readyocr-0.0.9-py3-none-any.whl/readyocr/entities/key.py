from readyocr.entities.bbox import BoundingBox
from readyocr.entities.textbox import TextBox


class Key(TextBox):
    """
    To create a new :class:`Key` object we need the following

    :param id: Unique identifier of the Key entity.
    :type id: str
    :param bbox: Bounding box of the Key entity.
    :type bbox: BoundingBox
    :param text: Transcription of the Key object.
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