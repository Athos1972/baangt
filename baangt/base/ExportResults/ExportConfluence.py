from atlassian import Confluence
from html import escape
import xlrd


class ExportConfluence:
    def __init__(self, url, space, pageTitle, fileNameAndPathToResultXLSX, username, password, rootPage=None,
                 remove_headers=["json"]):
        self.url = url
        self.space = space
        self.rootPage = rootPage
        self.pageTitle = pageTitle
        self.fileNameAndPathToResultXLSX = fileNameAndPathToResultXLSX
        self.username = username
        self.password = password
        self.remove_headers = [headers.lower() for headers in remove_headers]
        self.html = self.makeBody()
        #self.update_confluence()
        with open("test.html", 'w') as file:
            file.write(self.html)

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

    def xlsx2html(self, filePath, sheet):
        wb = xlrd.open_workbook(filePath)
        sht = wb.sheet_by_name(sheet)
        data = []  # used to store rows, which are later joined to make complete html
        remove_index = []  # used to store columns which are removable
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
                        dt.append(escape(value))
                else:
                    if column not in remove_index:  # if column is not in remove_header list than add the data in html
                        dt.append(escape(value))
            data.append('<td>' + '</td>\n<td>'.join(dt) + '</td>')  # joining individual data of a row in single row
        html = '<table>' + '<tr>' + '</tr>\n<tr>'.join(data) + '</tr>' + '</table>'  # joining list of rows to make html
        return html
