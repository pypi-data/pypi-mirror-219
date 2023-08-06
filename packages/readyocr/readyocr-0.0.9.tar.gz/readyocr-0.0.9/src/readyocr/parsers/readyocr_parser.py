from typing import Any, Dict, List, Tuple
from textractor.parsers.response_parser import parse

from readyocr.entities import BoundingBox, Word, Line, Paragraph, Block, Table, Cell, MergedCell, Key, Value, Page, Document
from readyocr.entities.entity_list import EntityList


# response = {
#     "document": {
#         "pages": [
#             {
#                 "id": "e6e56595-10cd-4984-b798-a0460ad0a0c3"
#                 "pageNumber": 1,
#                 "dimension": {
#                     "width": 1,
#                     "height": 0.9965640306472778,
#                     "unit": "pixel"
#                 },
#                 "entities": [
#                     {
#                         "id": "258e15b7-ada0-4f5e-87e4-ac0dfce8e7ff",
#                         "class": "Line",
#                         "boundingBox": {
#                             "x": 0.052512288093566895,
#                             "y": 0.8079520590823819,
#                             "width": 0.05254054814577103,
#                             "height": 0.009167630081129974
#                         },
#                         "metadata": {},
#                         "tags": [],
#                         "childrenIds": [
#                             "2aced2b4-a20a-427a-83d4-732f79ef378f",
#                             "1bb89b44-7a35-4466-bb21-0d0c6145c850"
#                         ],
#                         "text": "order of:",
#                         "confidence": 0.9911622619628906,
#                         "language": null
#                     },
#                 ]
#             }
#         ]
#     }
# }

def _create_document_object(response: dict) -> Document:
    """
    Consumes API Response in JSON format and creates a Document object.

    :param response: json response from Textract API
    :type response: dict

    :return: Returns a Document object populated with metadata on number of pages.
    :rtype: Document
    """
    doc = Document(num_pages=response.get("document", {}).get("num_pages", 0))
    return doc

def _create_object(entity_json):
    """_summary_

    :param entity_json: entity information json format
    -> Line: {
                "id": "258e15b7-ada0-4f5e-87e4-ac0dfce8e7ff",
                "class": "Line",
                "boundingBox": {
                    "x": 0.052512288093566895,
                    "y": 0.8079520590823819,
                    "width": 0.05254054814577103,
                    "height": 0.009167630081129974
                },
                "metadata": {},
                "tags": [],
                "childrenIds": [
                    "2aced2b4-a20a-427a-83d4-732f79ef378f",
                    "1bb89b44-7a35-4466-bb21-0d0c6145c850"
                ],
                "text": "order of:",
                "confidence": 0.9911622619628906,
                "language": null
            }
    -> Word: {
                "id": "ec5eac88-f05e-4fa2-9332-6745eeb4d95f",
                "class": "Word",
                "boundingBox": {
                    "x": 0.4973248541355133,
                    "y": 0.23672433135340398,
                    "width": 0.03262513503432274,
                    "height": 0.009943900668560324
                },
                "metadata": {},
                "tags": [],
                "childrenIds": [],
                "text": "date",
                "confidence": 0.9994115447998047,
                "language": null
            }
    -> Key: {
                "id": "ba26e843-759d-4abb-8f45-b75faf577553",
                "class": "Key",
                "boundingBox": {
                    "x": 0.5765600800514221,
                    "y": 0.3129917424933737,
                    "width": 0.0572432205080986,
                    "height": 0.010077135449113594
                },
                "metadata": {},
                "tags": [],
                "childrenIds": [
                    "b222e6e9-ba9a-47cb-acf9-7845d9ad3c11",
                    "890cbbcd-66d4-4d8d-a4f5-d6ee69c59288",
                    "b3929a99-ee32-4b64-8069-28fc7a822a81",
                    "aec8fc85-e5eb-4f12-af9a-b94c8e0c18a3"
                ],
                "text": "key",
                "confidence": 0.41478912353515623,
                "language": null
            }
    -> Value: {
                "id": "42de0ce2-8d7f-4573-af24-06eab2080e43",
                "class": "Value",
                "boundingBox": {
                    "x": 0.24050265550613403,
                    "y": 0.18935537547556613,
                    "width": 0.008100352250039577,
                    "height": 0.008480351599044478
                },
                "metadata": {},
                "tags": [],
                "childrenIds": [
                    "8f6bf718-d569-4941-b74e-f094a86a59dd"
                ],
                "text": "value",
                "confidence": 0.882987060546875,
                "language": null
            }
    :type entity_json: json
    """
    bbox = BoundingBox(entity_json['boundingBox']['x'], entity_json['boundingBox']['y'],
                       entity_json['boundingBox']['width'], entity_json['boundingBox']['height'])
    if entity_json['class'] == 'Table':
        entity = Table(id=entity_json['id'],
                       bbox=bbox,
                       confidence=1.0)
    elif entity_json['class'] == 'Cell':
        entity = Cell(id=entity_json['id'],
                      bbox=bbox,
                      row_index=entity_json['rowIndex'],
                      col_index=entity_json['columnIndex'],
                      text=entity_json['text'],
                      confidence=entity_json['confidence'])
    elif entity_json['class'] == 'MergedCell':
        entity = MergedCell(id=entity_json['id'],
                            bbox=bbox,
                            row_index=entity_json['rowIndex'],
                            col_index=entity_json['columnIndex'],
                            row_span=entity_json['rowSpan'],
                            col_span=entity_json['columnSpan'],
                            text=entity_json['text'],
                            confidence=entity_json['confidence'])
    elif entity_json['class'] in ('Word', 'Line', 'Key', 'Value'):
        entity = eval(entity_json['class'])(id=entity_json['id'],
                                            bbox=bbox,
                                            text=entity_json['text'],
                                            confidence=entity_json['confidence'])
    else:
        entity = None
    return entity


def load(response: dict) -> Document:
    """
    Convert ReadyOCR json to ReadyOCR document

    :param response: json response from readyocr
    :type response: dict
    :return: ReadyOCR document
    :rtype: Document
    """
    num_pages = len(response['document']['pages'])
    document = Document(num_pages=num_pages)
    for page_json in response['document']['pages']:
        # initialize page object
        page = Page(id=page_json['id'],
                    width=page_json['dimension']['width'],
                    height=page_json['dimension']['height'],
                    page_num=page_json['pageNumber'])
        # add entity into page
        for entity_json in page_json['entities']:
            entity = _create_object(entity_json=entity_json)
            page.add(entity)
        # linking entities
        for entity_json in page_json['entities']:
            parent_entity = page.children.get_by_id(entity_json['id'])
            for child_entity_id in entity_json['childrenIds']:
                child_entity = page.children.get_by_id(child_entity_id)
                parent_entity.add(child_entity)
        # add more things into page
        document.add(page)
    return document