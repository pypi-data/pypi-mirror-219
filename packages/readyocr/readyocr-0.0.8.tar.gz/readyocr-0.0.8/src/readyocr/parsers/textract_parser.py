from textractor.parsers.response_parser import parse

from readyocr.entities import BoundingBox, Word, Line, Table, Cell, MergedCell, Key, Value, Page, Document

def load(response: dict) -> Document:
    """
    Convert textract json to readyocr document

    :param response: json response from textract
    :type response: dict
    :return: readyocr document
    :rtype: Document
    """
    t_doc = parse(response)
    document = Document(num_pages=len(t_doc.pages))

    for t_page in t_doc.pages:
        page = Page(
            id=t_page.id,
            width=None,
            height=None,
            page_num=t_page.page_num
        )

        # Extract t_line t_word from textract and add to readyocr page
        for t_line in t_page.lines:
            line = Line(
                id=t_line.id,
                bbox=BoundingBox(
                    x=t_line.x,
                    y=t_line.y,
                    width=t_line.width,
                    height=t_line.height,
                ),
                text=t_line.text,
                confidence=t_line.confidence
            )
            page.children.add(line)

            for t_word in t_line.words:
                word = Word(
                    id=t_word.id,
                    bbox=BoundingBox(
                        x=t_word.x,
                        y=t_word.y,
                        width=t_word.width,
                        height=t_word.height,
                    ),
                    text=t_word.text,
                    confidence=t_word.confidence
                )
                line.children.add(word)

        # Extract t_key t_value from textract and add to readyocr page
        for t_key in t_page.key_values:
            t_value = t_key.value

            key = Key(
                id=t_key.id,
                bbox=BoundingBox(
                    x=t_key.x,
                    y=t_key.y,
                    width=t_key.width,
                    height=t_key.height,
                ),
                text='key',
                confidence=t_key.confidence
            )
            
            # add word to key
            for t_word in t_key.words:
                word = Word(
                    id=t_word.id,
                    bbox=BoundingBox(
                        x=t_word.x,
                        y=t_word.y,
                        width=t_word.width,
                        height=t_word.height,
                    ),
                    text=t_word.text,
                    confidence=t_word.confidence
                )

                key.children.add(word)

            value = Value(
                id=t_value.id,
                bbox=BoundingBox(
                    x=t_value.x,
                    y=t_value.y,
                    width=t_value.width,
                    height=t_value.height,
                ),
                text='value',
                confidence=t_value.confidence
            )

            # add word to value
            for t_word in t_value.words:
                word = Word(
                    id=t_word.id,
                    bbox=BoundingBox(
                        x=t_word.x,
                        y=t_word.y,
                        width=t_word.width,
                        height=t_word.height,
                    ),
                    text=t_word.text,
                    confidence=t_word.confidence
                )
                value.children.add(word)
            
            key.children.add(value)
            page.children.add(key)

        # Extract t_table, t_cell from textract and add to readyocr page
        for t_table in t_page.tables:
            table = Table(
                id=t_table.id,
                bbox=BoundingBox(
                    x=t_table.x,
                    y=t_table.y,
                    width=t_table.width,
                    height=t_table.height,
                ),
                confidence=1
            )

            # Add all normal table cell
            for t_cell in t_table.table_cells:
                cell = Cell(
                    id=t_cell.id,
                    bbox=BoundingBox(
                        x=t_cell.x,
                        y=t_cell.y,
                        width=t_cell.width,
                        height=t_cell.height,
                    ),
                    row_index=t_cell.row_index,
                    col_index=t_cell.col_index,
                    text=t_cell.text,
                    confidence=t_cell.confidence
                )
                
                if t_cell.is_column_header:
                    cell.tags.add('COLUMN_HEADER')
                if t_cell.is_title:
                    cell.tags.add('TITLE')
                if t_cell.is_footer:
                    cell.tags.add('FOOTER')
                if t_cell.is_summary:
                    cell.tags.add('SUMMARY')
                if t_cell.is_section_title:
                    cell.tags.add('SECTION_TITLE')

                for t_word in t_cell.words:
                    word = Word(
                        id=t_word.id,
                        bbox=BoundingBox(
                            x=t_word.x,
                            y=t_word.y,
                            width=t_word.width,
                            height=t_word.height,
                        ),
                        text=t_word.text,
                        confidence=t_word.confidence
                    )

                    cell.children.add(word)

                table.children.add(cell)
            
            page.children.add(table)

            # Add all merged table cell
            for t_cell in t_table.table_cells:
                if len(t_cell.siblings) > 0 and table.children.get_by_id(t_cell.parent_cell_id) is None:
                    x = min([x.x for x in t_cell.siblings])
                    y = min([x.y for x in t_cell.siblings])
                    width = max([x.x + x.width for x in t_cell.siblings]) - x
                    height = max([x.y + x.height for x in t_cell.siblings]) - y
                    row_index = min([x.row_index for x in t_cell.siblings])
                    col_index = min([x.col_index for x in t_cell.siblings])
                    row_span = max([x.row_index for x in t_cell.siblings]) - min([x.row_index for x in t_cell.siblings]) + 1
                    col_span = max([x.col_index for x in t_cell.siblings]) - min([x.col_index for x in t_cell.siblings]) + 1

                    merged_cell = MergedCell(
                        id=t_cell.parent_cell_id,
                        bbox=BoundingBox( 
                            x=x,
                            y=y,
                            width=width,
                            height=height,
                        ),
                        row_index=row_index,
                        col_index=col_index,
                        row_span=row_span,
                        col_span=col_span,
                        text='',
                        confidence=1
                    )
                    
                    for x in table.children:
                        if x.id in [x.id for x in t_cell.siblings]:
                            merged_cell.children.add(x)

                    table.children.add(merged_cell)

        document.pages.append(page)

    return document
