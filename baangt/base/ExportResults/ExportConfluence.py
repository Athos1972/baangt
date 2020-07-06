from atlassian import Confluence
from html import escape
import xlrd
import os


class ExportConfluence:
    def __init__(self, url, space, pageTitle, fileNameAndPathToResultXLSX, username, password, rootPage=None,
                 remove_headers=["json"], uploadOriginalFile=False):
        self.url = url
        self.space = space
        self.rootPage = rootPage
        self.pageTitle = pageTitle
        self.fileNameAndPathToResultXLSX = fileNameAndPathToResultXLSX
        self.username = username
        self.password = password
        self.remove_headers = [headers.lower() for headers in remove_headers]
        self.uploadOriginalFile = uploadOriginalFile
        self.html = self.makeBody()
        self.update_confluence()

    def makeBody(self):
        output = self.xlsx2html(self.fileNameAndPathToResultXLSX, sheet="Output")
        summary = self.xlsx2html(self.fileNameAndPathToResultXLSX, sheet="Summary")
        html = "<h1>Summary</h1>" + summary + "<br /><br /><h1>Output</h1>" + output
        html = html.replace('\\',  '\\\\')
        return html

    def update_confluence(self):
        confluence = Confluence(url=self.url, username=self.username, password=self.password)  # Confluence login
        confluence.create_page(
            self.space, self.pageTitle, self.html, parent_id=self.rootPage, type='page', representation='storage'
        )
        if self.uploadOriginalFile:
            file = self.attach_file(confluence)
            html = file + "<br /><br /><h1>Original file</h1>" + self.html

    def xlsx2html(self, filePath, sheet):
        wb = xlrd.open_workbook(filePath)
        sht = wb.sheet_by_name(sheet)
        data = []  # used to store rows, which are later joined to make complete html
        remove_index = []  # used to store columns which are removable
        header = []
        for row in range(sht.nrows):
            dt = []
            for column in range(sht.ncols):
                value = sht.cell_value(row, column)
                if type(value) == float:
                    if repr(value)[-2:] == '.0':
                        value = int(value)
                value = str(value)
                if row == 0:
                    if value.lower() in self.remove_headers:
                        remove_index.append(column)  # storing column number of removable headers in a list
                    else:
                        header.append(escape(value))
                else:
                    if column not in remove_index:  # if column is not in remove_header list than add the data in html
                        dt.append(escape(value))
            data.append('<td>' + '</td>\n<td>'.join(dt) + '</td>')  # joining individual data of a row in single row
        header = '<tr><th>' + '</th>\n<th>'.join(header) + '</th></tr>'
        html = '<table><tbody>' + header + '<tr>' + '</tr>\n<tr>'.join(data) + '</tr>' + '</tbody></table>'  # joining list of rows to make html
        return html

    def attach_file(self, confluence):
        fileName = os.path.basename(self.fileNameAndPathToResultXLSX)
        attach = confluence.attach_file(self.fileNameAndPathToResultXLSX, name=fileName, content_type=None,
                               page_id=self.rootPage, title=self.pageTitle, space=self.space, comment=None)
        history = confluence.get_attachments_from_content(self.rootPage, start=0, limit=50, expand=None, filename=fileName,
                                                media_type=None)
        link = f'<ac:link><ri:attachment ri:filename="{fileName}" />\
        <ac:plain-text-link-body><![CDATA[]]></ac:plain-text-link-body></ac:link>'
        html = "<h1>Original file</h1>"+link
        print(attach)
        print(history)
        return ""
