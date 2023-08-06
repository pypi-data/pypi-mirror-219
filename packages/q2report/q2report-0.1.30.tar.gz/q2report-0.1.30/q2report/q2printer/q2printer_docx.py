#    Copyright © 2021 Andrei Puchko
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

if __name__ == "__main__":  # pragma: no cover
    import sys

    sys.path.insert(0, ".")
    from demo.demo import demo

    demo()


from q2report.q2printer.q2printer import Q2Printer
from q2report.q2printer.docx_parts import docx_parts
from q2report.q2utils import num, int_, reMultiSpaceDelete
import zipfile
import base64

points_in_mm = 2.834645669
points_in_cm = num(points_in_mm) * num(10)
twip_in_cm = num(points_in_cm) * num(20)


class Q2PrinterDocx(Q2Printer):
    def __init__(self, output_file, output_type=None):
        super().__init__(output_file, output_type)
        self.document = []
        self.xmlImageList = []
        self.images_size_list = []
        self.document.append(docx_parts["doc_start"])
        self.page_params = None

        self.current_page_header = None
        self.headers = []

        self.current_page_footer = None
        self.footers = []

        self.table_opened = False

    def save(self):
        super().save()
        self.close_docx_page(True)
        self.document.append("</w:body>")
        self.document.append("</w:document>")

        zipf = zipfile.ZipFile(self.output_file, "w", zipfile.ZIP_DEFLATED)

        document_xml_rels = []

        # images
        for x in range(len(self.xmlImageList)):
            zipf.writestr("word/media/image%s.png" % x, base64.b64decode(self.xmlImageList[x]))
            document_xml_rels.append(docx_parts["images"] % (x, x))

        # headers
        document_xml_headers = []
        headers_footers_content_types = []
        for pos, x in enumerate(self.headers):
            zipf.writestr("word/header%s.xml" % pos, x)
            document_xml_headers.append(docx_parts["headers"] % (self.get_header_rid(len(self.headers)), pos))
            headers_footers_content_types.append(
                docx_parts["headers_footers_content_type"] % ("header", pos, "header")
            )

            zipf.writestr(
                "word/_rels/header%s.xml.rels" % pos,
                docx_parts["word_rels"] % "".join(document_xml_rels),
            )

        # footers
        document_xml_footers = []
        for pos, x in enumerate(self.footers):
            zipf.writestr("word/footer%s.xml" % (pos + 200), x)
            document_xml_footers.append(docx_parts["footers"] % (pos + 200, pos + 200))
            headers_footers_content_types.append(
                docx_parts["headers_footers_content_type"] % ("footer", pos + 200, "footer")
            )

            zipf.writestr(
                "word/_rels/footer%s.xml.rels" % (pos + 200),
                docx_parts["word_rels"] % "".join(document_xml_rels),
            )

        document_xml_rels.extend(document_xml_headers)
        document_xml_rels.extend(document_xml_footers)
        zipf.writestr("word/_rels/document.xml.rels", docx_parts["word_rels"] % "".join(document_xml_rels))

        zipf.writestr("_rels/.rels", docx_parts["rels"])

        content_type = "\n".join(headers_footers_content_types)
        zipf.writestr("[Content_Types].xml", docx_parts["content_type"] % content_type)

        zipf.writestr("word/document.xml", "".join(self.document).encode("utf8"))
        zipf.close()

    def reset_page(
        self,
        page_width=21,
        page_height=29,
        page_margin_left=2,
        page_margin_top=1,
        page_margin_right=1,
        page_margin_bottom=1,
    ):

        self.close_docx_page()

        super().reset_page(
            page_width,
            page_height,
            page_margin_left,
            page_margin_top,
            page_margin_right,
            page_margin_bottom,
        )

        self.page_params = True

    def close_docx_page(self, last_page=False):
        self.close_docx_table()
        if self.page_params:
            header_ref_xml = ""
            footer_ref_xml = ""
            if self.current_page_header:
                self.headers.append(self.current_page_header)
                self.current_page_header = None
                header_ref_xml = """<w:headerReference w:type="default" r:id="rId%s"/>""" % (
                    self.get_header_rid(len(self.headers))
                )

            if self.current_page_footer:
                self.footers.append(self.current_page_footer)
                self.current_page_footer = None
                footer_ref_xml = """<w:footerReference w:type="default" r:id="rId%s"/>""" % (
                    len(self.footers) + 200 - 1
                )

            page_param_xml = self.page_parm_xml(header_ref_xml, footer_ref_xml, last_page)

            self.document.append(page_param_xml)

    def get_header_rid(self, id):
        return f"_header_{id}"

    def get_footer_rid(self, id):
        return f"_footer_{id}"

    def page_parm_xml(self, header_ref_xml, footer_ref_xml, last_page):
        if last_page:
            pre_page_param = "%s"
        else:
            pre_page_param = """
                <w:p>
                    <w:pPr>
                    %s
                    <w:rPr/>
                    </w:pPr>
                <w:r>
                    <w:rPr/>
                </w:r>
                <w:r>
                    <w:br w:type="page"/>
                </w:r>
            </w:p>
            """
        page_param = f"""
                        <w:sectPr>
                            {header_ref_xml}
                            {footer_ref_xml}
                            <w:type w:val="nextPage"/>
                            <w:pgSz
                                w:w="{self.page_width * twip_in_cm}"
                                w:h="{self.page_height * twip_in_cm}"/>
                            <w:pgMar w:gutter="0" w:header="708" w:footer="708"
                                    w:top="{self.page_margin_top * twip_in_cm}"
                                    w:right="{self.page_margin_right * twip_in_cm}"
                                    w:bottom="{self.page_margin_bottom * twip_in_cm}"
                                    w:left="{self.page_margin_left * twip_in_cm}"
                            />
                            <w:cols w:space="708"/>
                            <w:docGrid w:linePitch="360"/>
                            <w:formProt w:val="false"/>
                            <w:textDirection w:val="lrTb"/>
                        </w:sectPr>
                """
        page_param_xml = pre_page_param % page_param

        return page_param_xml

    def reset_columns(self, widths=None):
        self.close_docx_table()
        if widths:
            super().reset_columns(widths)
        self.open_docx_table()

    def open_docx_table(self):
        self.document.append(self.open_docs_table_xml())
        self.table_opened = True

    def close_docx_table(self):
        if self._columns_count and self.table_opened:
            self.document.append("</w:tbl>\n")
            self.document.append("<w:p><w:r><w:rPr/></w:r></w:p>\n")
            self.table_opened = False

    def open_docs_table_xml(self):
        open_docs_table_xml = []
        open_docs_table_xml.append(
            f"""<w:tbl>
                    <w:tblPr>
                        <w:tblLayout w:type="fixed"/>
                        <w:tblInd w:w="28" w:type="dxa"/>
                        <w:tblW w:w="{round(sum(int_(x * twip_in_cm) for x in self._cm_columns_widths))}"
                             w:type="dxa"/>
                        <w:tblCellMar>
                            <w:top w:w="28" w:type="dxa"/>
                            <w:left w:w="28" w:type="dxa"/>
                            <w:bottom w:w="28" w:type="dxa"/>
                            <w:right w:w="28" w:type="dxa"/>
                        </w:tblCellMar>
                    </w:tblPr>
                    <w:tblGrid>\n"""
        )
        for col in self._cm_columns_widths:
            open_docs_table_xml.append(f'\t\t<w:gridCol w:w="{int_(col * twip_in_cm)}"/>\n')
        open_docs_table_xml.append("""\t</w:tblGrid>\n""")
        return "\n".join(open_docs_table_xml)

    def render_rows_section(self, rows_section, style, outline_level):
        super().render_rows_section(rows_section, style, outline_level)
        spanned_cells_first_column_cell = {}
        spanned_cells_empty_column_cell = {}
        if rows_section["role"] == "table_header":
            self.reset_columns()

        row_section_xml = []

        if rows_section["role"] in ("header", "footer"):
            row_section_xml.append(self.open_docs_table_xml())

        for row in range(len(rows_section["heights"])):  # вывод - по строкам
            row_section_xml.append(self.open_table_row(row, rows_section))

            for col in range(self._columns_count):  # цикл по клеткам строки
                key = f"{row},{col}"
                if key in spanned_cells_empty_column_cell:
                    continue

                cell_data = rows_section.get("cells", {}).get(key, {})

                cell_text = cell_data.get("data", "")
                row_span = cell_data.get("rowspan", 1)
                col_span = cell_data.get("colspan", 1)
                cell_style = cell_data.get("style", {})
                if cell_data.get("width"):
                    cell_width = cell_data["width"]
                else:
                    cell_width = self._cm_columns_widths[col]

                if cell_style == {}:
                    cell_style = dict(style)
                if key in spanned_cells_first_column_cell:
                    row_section_xml.append(
                        self.add_table_cell(cell_style, "", cell_width, spanned_cells_first_column_cell[key])
                    )
                    continue

                merge_str = ""
                if row_span > 1 or col_span > 1:
                    if col_span > 1:
                        merge_str = f'<w:gridSpan w:val="{col_span}"/>'
                    for tmp_span_row in range(int_(row_span)):
                        for tmp_span_col in range(int_(col_span)):
                            span_key = f"{tmp_span_row+row},{tmp_span_col+col}"
                            if tmp_span_row + row != row and tmp_span_col + col == col:
                                spanned_cells_first_column_cell[
                                    span_key
                                ] = f'{merge_str} <w:vMerge w:val="continue"/>'
                            if tmp_span_col + col > col:
                                spanned_cells_empty_column_cell[span_key] = ""

                    if row_span > 1:
                        merge_str += '<w:vMerge w:val="restart"/>'

                row_section_xml.append(
                    self.add_table_cell(
                        cell_style,
                        cell_text,
                        cell_width,
                        merge_str,
                        self.get_cell_images(cell_data),
                    )
                )

            row_section_xml.append(self.close_table_row())

        if rows_section["role"] == "header":
            row_section_xml.append("</w:tbl>\n")
            self.current_page_header = docx_parts["header"] % ("".join(row_section_xml))
        elif rows_section["role"] == "footer":
            row_section_xml.append("</w:tbl>\n")
            self.current_page_footer = docx_parts["footer"] % ("".join(row_section_xml))
        else:
            self.document.extend(row_section_xml)

    def get_cell_images(self, cell_data):
        images_list = cell_data.get("images")
        cell_width = cell_data.get("width")
        cell_images_list = []
        if not images_list:
            return ""
        for x in images_list:
            width, height, imageIndex = self.prepare_image(x, cell_width)

            width = round(num(width) * num(12700) * points_in_cm)
            height = round(num(height) * num(12700) * points_in_cm)

            cell_images_list.append(docx_parts["image"] % locals())
        return "\n".join(cell_images_list)

    def open_table_row(self, row, rows):
        row_xml = ""
        row_xml += "\n\t<w:tr>"
        row_xml += "\n\t\t<w:trPr>"
        if rows["role"] == "table_header":
            row_xml += "<w:tblHeader/>"
        # if rows["docx_height"][row]:
        #     row_xml += f'\n\t\t\t<w:trHeight w:val="{rows["docx_height"][row]*twip_in_cm}" w:hRule="exact"/>'
        row_xml += "\n\t\t</w:trPr>"
        return row_xml

    def close_table_row(self):
        return "\n\t</w:tr>"

    def add_table_cell(self, cell_style, cell_text, cell_width, merge_str, images=[]):
        borders = self.get_cell_borders(cell_style)
        margins = self.get_cell_paddings(cell_style)
        para_params = self.get_paragraph_params(cell_style)
        para_text = self.get_paragraph_text(cell_style, cell_text, para_params)
        valign = self.get_vertical_align(cell_style)

        # self.document.append(
        return f"""
                <w:tc>
                    <w:tcPr>
                        <w:tcW w:w="{int(cell_width * twip_in_cm)}" w:type="dxa"/>
                        {valign}
                        {merge_str}
                        {borders}
                        {margins}
                    </w:tcPr>
                    <w:p>
                        {para_params}
                        {para_text}
                        {images}
                    </w:p>
                </w:tc>
        """

    def get_paragraph_text(self, cell_style, cell_text, para_params):
        cell_text = cell_text.replace("\n", "")
        cell_text = cell_text.replace("\r", "")
        cell_text = reMultiSpaceDelete.sub(" ", cell_text)
        para_text = []
        if "font-weight" in cell_style and cell_style["font-weight"] == "bold":
            cell_text = f"<b>{cell_text}</b>"
        bold = ""
        ital = ""
        undl = ""
        fontsizemod = fontsize = num(cell_style["font-size"].replace("pt", "")) * 2
        fontfamily = cell_style["font-family"]
        for x in cell_text.split("<"):
            if ">" in x:
                stl = x.split(">")[0].upper().strip().replace(" ", "")
                if "B" == stl:
                    bold = "<w:b/>"
                elif "/B" == stl:
                    bold = ""
                elif "I" == stl:
                    ital = "<w:i/>"
                elif "/I" == stl:
                    ital = ""
                elif "U" == stl:
                    undl = """<w:u w:val="single"/>"""
                elif "/U" == stl:
                    undl = ""
                elif "/FONT" in stl:
                    fontsizemod = fontsize
                # elif "FONTSIZE=" in stl:
                #     fontsizemod = grid.getFontSizeMod(fontsize / 2, stl.split("=")[1]) * 2
                elif "BR/" == stl or "BR" == stl:
                    para_text.append(f"""</w:p><w:p>{para_params}""")
                    # para_text.append(self.get_paragraph_params(cell_style))
                x = x.split(">")[1]
            if x:
                para_text.append(
                    f"""
                    <w:r>
                        <w:rPr>
                            <w:rFonts w:ascii="{fontfamily}" w:hAnsi="{fontfamily}" w:cs="{fontfamily}"/>
                            <w:sz w:val="{fontsizemod}"/>
                            {bold}{ital}{undl}
                        </w:rPr>
                        <w:t xml:space="preserve">{x}</w:t>
                    </w:r>
                    """
                )
        return "".join(para_text)

    def get_paragraph_params(self, cell_style):
        paragraph = f"""
<w:pPr>
\t{self.get_horizontal_align(cell_style)}
\t<w:widowControl w:val="0"/>
\t<w:adjustRightInd w:val="0"/>
\t<w:autoSpaceDE w:val="0"/>
\t<w:autoSpaceDN w:val="0"/>
\t<w:spacing w:before="0" w:after="0" w:lineRule="atLeast" w:line="0"/>
</w:pPr>"""
        return paragraph

    def get_vertical_align(self, cell_style):
        if cell_style["vertical-align"] == "middle":
            vert_align = '<w:vAlign w:val="center"/>'
        elif cell_style["vertical-align"] == "bottom":
            vert_align = '<w:vAlign w:val="bottom"/>'
        else:
            vert_align = ""
        return vert_align

    def get_horizontal_align(self, cell_style):
        if cell_style["text-align"] == "center":
            hor_align = '<w:jc w:val="center"/>'
        elif cell_style["text-align"] == "right":
            hor_align = '<w:jc w:val="right"/>'
        elif cell_style["text-align"] == "justify":
            hor_align = '<w:jc w:val="both"/>'
        else:
            hor_align = ""
        return hor_align

    def get_cell_borders(self, cell_style):
        border_width = cell_style["border-width"].split(" ")
        while len(border_width) < 4:
            border_width += border_width
        borders = []
        borders.append("<w:tcBorders>\n")
        for index, side in enumerate(("top", "right", "bottom", "left")):
            if int_(border_width[index]):
                borders.append(f'\t\t\t<w:{side} w:val="single" w:color="auto" w:space="0"')
                borders.append(f'\t\t\t\tw:sz="{int_(border_width[index])*10}"/>')
        borders.append("</w:tcBorders>\n")
        return "\n".join(borders)

    def get_cell_paddings(self, cell_style):
        padding = cell_style["padding"].replace("cm", "").split(" ")
        while len(padding) < 4:
            padding += padding
        margins = []
        margins.append("\n\t<w:tcMar>")
        for index, side in enumerate(("top", "right", "bottom", "left")):
            margins.append(f'\n\t\t<w:{side} w:w="{int(num(padding[index])*twip_in_cm)}" w:type="dxa"/>')
        margins.append("\n\t</w:tcMar>\n")
        return "".join(margins)
