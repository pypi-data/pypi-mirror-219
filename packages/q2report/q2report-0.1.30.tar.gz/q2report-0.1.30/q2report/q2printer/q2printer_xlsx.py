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
from q2report.q2printer.xlsx_parts import xlsx_parts
from q2report.q2utils import num, int_, reMultiSpaceDelete

import zipfile
import re
import base64

reSpaces = re.compile(r"\s*", re.IGNORECASE)
reFormula = re.compile(r"\[[^]^[]+\]")
reFloat = re.compile(r"[-+]?\d*\.\d+|\d+")
reHtmlTagBr = re.compile(r"<\s*/*BR\s*/*\s*>", re.IGNORECASE)
reHtmlTagFontSize = re.compile(r"\s*font\s*size\s*\=", re.IGNORECASE)
reHtmlTagFontEnd = re.compile(r"\<\s*/\s*font\s*>", re.IGNORECASE)
reFontSize = re.compile(r"\<\s*font\s+size\\s*=\s*[+-]*\s*[0-9]*\s*\>", re.IGNORECASE)
reSignAndSize = re.compile(r"[+-]*\s*[0-9]+")
rePixMap = re.compile(r"zzPixmap\s*\(\s*.*\s*\)")
reIsoDate = re.compile(r"^(?P<date>(\d\d\d\d\-((0[1-9])|(1(0|1|2))))\-((0[1-9])|(1\d)|(2\d)|(3(0|1))))$")
reFontModifiers = re.compile(r"\<(\/*b)|(br/)|(font)|(\/*u)|(\/*i)\>", re.IGNORECASE)


reSubFontSize = re.compile(r"(<(\s*font\s+size\s*=\s*[+-]*\s*\d+\s*)>)", re.IGNORECASE)
reSubFontEnd = re.compile(r"(<(\s*\/\s*font\s*)>)", re.IGNORECASE)
reSubBold = re.compile(r"(<(\s*b\s*)>)", re.IGNORECASE)
reSubBoldEnd = re.compile(r"(<(\s*\/\s*b\s*)>)", re.IGNORECASE)
reSubItalic = re.compile(r"(<(\s*i\s*)>)", re.IGNORECASE)
reSubItalicEnd = re.compile(r"(<(\s*\/\s*i\s*)>)", re.IGNORECASE)
reSubUnderline = re.compile(r"(<(\s*u\s*)>)", re.IGNORECASE)
reSubUnderlineEnd = re.compile(r"(<(\s*\/\s*u\s*)>)", re.IGNORECASE)


reUnderLineBegin = re.compile(r"<\s*u\s*>", re.IGNORECASE)
reUnderLineEnd = re.compile(r"<\s*/\s*U\s*>", re.IGNORECASE)

cm_2_inch = num(2.5396)
points_in_mm = num(2.834645669)
points_in_cm = num(points_in_mm) * num(10)
twip_in_cm = num(points_in_cm) * num(20)


class Q2PrinterXlsx(Q2Printer):
    def __init__(self, output_file, output_type=None):
        super().__init__(output_file, output_type)
        self.xlsx_sheets = []
        self.current_sheet = {}
        self.sheet_current_row = 1

        self.fonts = ["""<sz val="11"/><name val="Calibri"/>"""]
        self.fills = ["""<patternFill patternType="none"/>"""]
        self.borders = ["""<left/><right/><top/><bottom/><diagonal/>"""]
        self.cell_xfs = ["""<xf borderId="0" fillId="0" fontId="0" numFmtId="0" xfId="0"/>"""]
        self.xmlImageList = []
        self.images_size_list = []

        self.cellStyleXfs = []
        self.cellStyles = []
        self.sharedStrings = []

        self.html = []
        self.style = {}

    def save(self):
        self.close_xlsx_sheet()
        super().save()

        # zipf = zipfile.ZipFile(self.output_file + ".zip", "w", zipfile.ZIP_DEFLATED)
        zipf = zipfile.ZipFile(self.output_file, "w", zipfile.ZIP_DEFLATED)
        zipf.writestr(
            "xl/sharedStrings.xml",
            (
                xlsx_parts["xl/sharedStrings.xml"]
                % (
                    len(self.sharedStrings),
                    len(self.sharedStrings),
                    "".join("""<si>%s</si>\n""" % st for st in self.sharedStrings),
                )
            ).encode("utf8"),
        )
        zipf.writestr("_rels/.rels", xlsx_parts["_rels/.rels"].encode("utf8"))
        self.save_styles(zipf)

        wb_sheets = []
        wb_workbook_rels = []
        wb_images = []
        wb_content_types = []

        for img in range(0, len(self.xmlImageList)):
            zipf.writestr(r"xl\media\image%s.png" % (img + 1), base64.b64decode(self.xmlImageList[img]))
            wb_images.append(xlsx_parts["images"] % ((img + 1), (img + 1)))

        for x in range(0, len(self.xlsx_sheets)):
            wb_content_types.append(xlsx_parts["wb_content_types_sheet"] % (x + 1))
            drawing_det = []
            if self.xlsx_sheets[x]["drawing"]:
                for img in range(0, len(self.xlsx_sheets[x]["drawing"])):
                    drawing_det.append(
                        xlsx_parts["xl/drawings/drawing.xml(png)"] % self.xlsx_sheets[x]["drawing"][img]
                    )

            zipf.writestr(
                "xl/drawings/_rels/drawing%s.xml.rels" % (x + 1),
                xlsx_parts["xl/drawings/_rels/drawing.xml.rels"] % "".join(wb_images),
            )
            zipf.writestr(
                "xl/drawings/drawing%s.xml" % (x + 1),
                (xlsx_parts["xl/drawings/drawing.xml"] % "".join(drawing_det)),
            )

            if drawing_det:
                wb_content_types.append(xlsx_parts["wb_content_types_image"] % (x + 1))
                zipf.writestr(
                    "xl/worksheets/_rels/sheet%s.xml.rels" % (x + 1),
                    (xlsx_parts["xl/worksheets/_rels/sheet.xml.rels"] % (x + 1)),
                )
                drawing = '<drawing r:id="rId1"/>'
            else:
                drawing = ""

            wb_sheets.append(
                """\
                    <sheet name="Sheet%s" sheetId="%s" r:id="rId%s"/>"""
                % (x + 1, x + 1, x + 9)
            )
            wb_workbook_rels.append(xlsx_parts["xl/_rels/workbook.xml.rels-line"] % (x + 9, x + 1))

            #             sheet_data = "".join(
            #                 """
            # <row r="%s" customHeight="1" ht="%s" outlineLevel="%s" collapsed="false"> %s \n
            # </row>"""
            #                 % (
            #                     z + 1,
            #                     self.xlsx_sheets[x]["sheetData"][z]["height"],
            #                     self.xlsx_sheets[x]["sheetData"][z]["outline_level"],
            #                     "".join(self.xlsx_sheets[x]["sheetData"][z]["cells"]),
            #                 )
            #                 for z in range(len(self.xlsx_sheets[x]["sheetData"]))
            #             )

            sheet_data = "".join(
                f"""
                    <row
                    \tr="{z+1}"
                    \tcustomHeight="1" ht="{self.xlsx_sheets[x]["sheetData"][z]["height"]}"
                    \toutlineLevel="{self.xlsx_sheets[x]["sheetData"][z]["outline_level"]}"
                    collapsed="false"
                    >
                    {"".join(self.xlsx_sheets[x]["sheetData"][z]["cells"])}
                    </row>"""
                for z in range(len(self.xlsx_sheets[x]["sheetData"]))
            )

            merges = "".join(self.xlsx_sheets[x]["spans"])
            if merges:
                merges = """<mergeCells count="%s">%s\n</mergeCells>""" % (
                    len(self.xlsx_sheets[x]["spans"]),
                    merges,
                )
            zipf.writestr(
                "xl/worksheets/sheet%s.xml" % (x + 1),
                (
                    xlsx_parts["xl/worksheets/sheet.xml"]
                    % (self.xlsx_sheets[x]["cols"], sheet_data, merges, self.xlsx_sheets[x]["page"], drawing)
                ),
            )

        zipf.writestr(
            "xl/_rels/workbook.xml.rels",
            (xlsx_parts["xl/_rels/workbook.xml.rels"] % "".join(wb_workbook_rels)).encode("utf8"),
        )

        zipf.writestr("xl/workbook.xml", (xlsx_parts["xl/workbook.xml"] % "".join(wb_sheets)).encode("utf8"))

        zipf.writestr(
            "[Content_Types].xml",
            (xlsx_parts["[Content_Types].xml"] % "".join(wb_content_types)).encode("utf8"),
        )

        zipf.close()

    def reset_columns(self, widths):
        super().reset_columns(widths)
        self.close_xlsx_sheet()

        self.sheet_current_row = 1
        self.current_sheet = {}
        self.current_sheet["drawing"] = []

        cols = ["<cols>"]
        for col_index, col in enumerate(self._cm_columns_widths):
            cols.append(
                f'\n\t<col min="{col_index+1}" max="{col_index+1}" '
                f' width="{col * num(5.105)}" bestFit="0" customWidth="1"/>'
            )
        cols.append("\n</cols>")
        self.current_sheet["cols"] = "".join(cols)

        self.current_sheet["page"] = (
            f"<pageMargins "
            f'\nleft="{round(self.page_margin_left / cm_2_inch,4)}" '
            f'\nright="{round((self.page_margin_right-num(0.01)) / cm_2_inch,4)}" '
            f'\ntop="{round(self.page_margin_top / cm_2_inch,4)}" '
            f'\nbottom="{round(self.page_margin_bottom / cm_2_inch,4)}" '
            f'\nheader="0.3" '
            f'\nfooter="0.3"/> '
            f'\n\n<pageSetup paperSize="0" '
            f' paperHeight="{self.page_height}cm" paperWidth="{self.page_width}cm" '
            f"""orientation="{'landscape' if self.page_width > self.page_height else 'portrait'}"/>"""
        )
        self.current_sheet["sheetData"] = []
        self.current_sheet["spans"] = []

    def close_xlsx_sheet(self):
        if self.current_sheet:
            self.xlsx_sheets.append(self.current_sheet)

    def render_rows_section(self, rows_section, style, outline_level):
        super().render_rows_section(rows_section, style, outline_level)
        row_count = len(rows_section["heights"])
        spanned_cells = {}

        sheet_row = {}
        for row in range(row_count):  # вывод - по строкам
            # sheet_row["height"] = (
            #     rows_section["real_heights"][row] if rows_section["real_heights"][row] else num(0.7)
            # ) * points_in_cm

            sheet_row["height"] = rows_section["max_cell_height"][row] * points_in_cm
            sheet_row["cells"] = []
            sheet_row["outline_level"] = outline_level
            for col in range(self._columns_count):  # цикл по клеткам строки
                key = f"{row},{col}"
                if key in spanned_cells:
                    sheet_row["cells"].append(spanned_cells[key])
                    continue
                cell_address = self.get_cell_address(self.sheet_current_row, col)
                cell_data = rows_section.get("cells", {}).get(key, {})
                cell_text = cell_data.get("data", "")

                row_span = cell_data.get("rowspan", 1)
                col_span = cell_data.get("colspan", 1)

                cell_style = cell_data.get("style", {})
                if cell_style == {}:
                    cell_style = dict(style)
                    # cell_data["style"] = cell_style

                self.make_image(cell_data, row, col)
                cell_xml = self.make_xlsx_cell(cell_address, cell_style, cell_text, cell_data)
                sheet_row["cells"].append(cell_xml)
                if row_span > 1 or col_span > 1:
                    merge_str = ":".join(
                        (
                            self.get_cell_address(self.sheet_current_row, col),
                            self.get_cell_address(self.sheet_current_row + row_span - 1, col + col_span - 1),
                        )
                    )
                    self.current_sheet["spans"].append(f'\n\t<mergeCell ref="{merge_str}"/>')
                    for span_row in range(int_(row_span)):
                        for span_col in range(int_(col_span)):
                            cell_address = self.get_cell_address(
                                self.sheet_current_row + span_row, span_col + col
                            )
                            spanned_cells[f"{span_row+row},{span_col+col}"] = self.make_xlsx_cell(
                                cell_address, cell_style, ""
                            )
            self.current_sheet["sheetData"].append(dict(sheet_row))
            self.sheet_current_row += 1

    def save_styles(self, zipf):
        borders = """<borders count="%s">%s</borders>\n""" % (
            len(self.borders),
            "".join("\n<border>%s</border>" % x for x in self.borders),
        )
        fonts = """<fonts count="%s">%s</fonts>\n""" % (
            len(self.fonts),
            "".join("\n<font>%s</font>" % font for font in self.fonts),
        )
        cellXfs = """\n<cellXfs count="%s">%s\n</cellXfs>""" % (
            len(self.cell_xfs),
            "".join("\n%s" % style for style in self.cell_xfs),
        )

        zipf.writestr("xl/styles.xml", (xlsx_parts["xl/styles.xml"] % locals()).encode("utf8"))

    def get_cell_xf_id(self, style, numFmtId=0):
        border = f'borderId="{self.get_cell_borders(style)}"'
        fill = f'fillId="{0}"'
        font = f'fontId="{self.get_font_id(style)}"'
        num_fmt = f'numFmtId="{numFmtId}"'
        align = self.get_cell_align(style)

        cell_xfs = f'<xf {border} {fill} {font} {num_fmt} xfId="0" applyAlignment="true"> {align} </xf>'
        if cell_xfs not in self.cell_xfs:
            self.cell_xfs.append(cell_xfs)
        xf_id = self.cell_xfs.index(cell_xfs)

        return xf_id

    def get_font_id(self, style):
        font_size = num(style["font-size"].replace("pt", ""))
        font_family = style["font-family"]
        font_weight = "<b/>" if style.get("font-weight", "") == "bold" else ""
        font_style = """<name val="%s"/> <sz val="%s"/>%s""" % (font_family, font_size, font_weight)
        if font_style not in self.fonts:
            self.fonts.append(font_style)
        #     font_id = len(self.fonts) - 1
        # else:
        font_id = self.fonts.index(font_style)
        return font_id

    def make_image(self, cell_data, row, col):
        for x in cell_data.get("images", []):
            width, height, imageIndex = self.prepare_image(x, cell_data.get("width"))

            width = num(width) * num(12700) * points_in_cm
            height = num(height) * num(12700) * points_in_cm

            tmp_drawing = {}
            tmp_drawing["_id"] = imageIndex + 1
            tmp_drawing["_row"] = self.sheet_current_row - 1
            tmp_drawing["_col"] = col
            tmp_drawing["_height"] = int(height)
            tmp_drawing["_width"] = int(width)
            self.current_sheet["drawing"].append(tmp_drawing)

    def make_xlsx_cell(self, cell_address, cell_style, cell_text, cell_data={}):
        if cell_data.get("numFmtId"):
            xf_id = self.get_cell_xf_id(cell_style, cell_data.get("numFmtId"))
            return f"""\n\t<c r="{cell_address}"
                            s="{xf_id}"
                            t="n">
                    <v>{cell_data.get("xlsx_data")}</v>
                    \n\t</c>"""

        fontsizemod = fontsize = cell_style["font-size"].replace("pt", "")
        fontfamily = cell_style["font-family"]

        cell_content = []
        cell_text = cell_text.replace("\n", "")
        cell_text = cell_text.replace("\r", "")
        cell_text = reMultiSpaceDelete.sub(" ", cell_text)
        cell_text = reHtmlTagBr.sub("\n", cell_text)
        if re.findall(r"\<(\/*b)|(br/)|(font)|(u)|(i)\>", cell_text, re.IGNORECASE):
            bold = ""
            ital = ""
            undl = ""
            for x in cell_text.split("<"):
                if ">" in x:
                    stl = x.split(">")[0].upper().strip().replace(" ", "")
                    if "B" == stl:
                        bold = "<b/>"
                    elif "/B" == stl:
                        bold = ""
                    elif "I" == stl:
                        ital = "<i/>"
                    elif "/I" == stl:
                        ital = ""
                    elif "U" == stl:
                        undl = """<u/>"""
                    elif "/U" == stl:
                        undl = ""
                    elif "/FONT" in stl:
                        fontsizemod = fontsize
                    # elif "FONTSIZE=" in stl:
                    #     fontsizemod = grid.getFontSizeMod(fontsize / 2, stl.split("=")[1])
                    x = x.split(">")[1]
                if x.strip():
                    cell_content.append(
                        f"""<r>
                                <rPr>
                                    <rFont val="{fontfamily}"/>
                                    <sz val="{fontsizemod}"/>{bold}{ital}{undl}
                                </rPr><t xml:space="preserve">{x}</t>
                            </r>"""
                    )
        elif cell_text != "":
            cell_content.append(f'<t xml:space="preserve">{cell_text}</t>')

        xf_id = self.get_cell_xf_id(cell_style)

        if cell_content:
            cell_content = "".join(cell_content)
            if cell_content not in self.sharedStrings:
                self.sharedStrings.append(cell_content)
                shared_strings_id = len(self.sharedStrings) - 1
            else:
                shared_strings_id = self.sharedStrings.index(cell_content)
            return f"""\n\t<c r="{cell_address}"
                            s="{xf_id}"
                            t="s">
                    \n\t\t<v>{shared_strings_id}</v>
                    \n\t</c>"""
            # return (
            #     f'''\n\t<c r="{cell_address}"
            #                 s="2"
            #                 t="n">
            #         <v>123</v>
            #         \n\t</c>'''
            # )
        else:
            return f'\n\t<c r="{cell_address}" s="{xf_id}"/> '

    def get_cell_align(self, cell_style):

        if cell_style["vertical-align"] == "middle":
            vertical = 'vertical="center"'
        elif cell_style["vertical-align"] == "top":
            vertical = 'vertical="top"'
        else:
            vertical = ""

        padding = cell_style["padding"].replace("cm", "").split(" ")
        while len(padding) < 4:
            padding += padding

        if cell_style["text-align"] == "center":
            horizontal = 'horizontal="center"'
        elif cell_style["text-align"] == "right":
            horizontal = 'horizontal="right"'
            if padding[1]:
                horizontal += f""" indent="{int(round(num(padding[1]) / num(0.25)))}" """
        elif cell_style["text-align"] == "justify":
            horizontal = 'horizontal="justify"'
        else:
            horizontal = ""
            if padding[3]:
                horizontal = f""" horizontal="left" indent="{int(round((num(padding[3])) / num(0.25)))}" """
        return f'\n\t<alignment {horizontal} {vertical} wrapText="true"/>\n'

    def get_cell_borders(self, style):
        border_width = style["border-width"].split(" ")
        while len(border_width) < 4:
            border_width += border_width
        border = []
        for index, side in enumerate(("left", "right", "top", "bottom")):
            if int_(border_width[index]):
                bw = self.get_border_width(border_width[index])
                border.append(f'<{side} style="{bw}"><color auto="1"/></{side}>')
        border.append("<diagonal/>")

        borders = "\n".join(border)

        if borders not in self.borders:
            self.borders.append(borders)
            border_id = len(self.borders) - 1
        else:
            border_id = self.borders.index(borders)
        return border_id

    def get_border_width(self, borderWidth):
        borderWidth = num(borderWidth)
        if borderWidth == 1:
            return "thin"
        elif borderWidth <= 3:
            return "medium"
        elif borderWidth > 3:
            return "thick"

    def get_cell_address(self, row, col):
        return self.get_xls_column_letter(col + 1) + str(row)

    def get_xls_column_letter(self, col):
        rez = ""
        while col:
            part = col % 26
            if part == 0:
                part = 26
            col = int((col - 1) / 26)
            rez = chr(ord("A") + part - 1) + rez
        return rez
