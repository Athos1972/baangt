from bs4 import BeautifulSoup as bs
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
        with open("test.html", 'w')as file:
            file.write(self.html)

    def makeBody(self):
        output = self.xlsx2html(self.fileNameAndPathToResultXLSX, sheet="Output")
        summary = self.xlsx2html(self.fileNameAndPathToResultXLSX, sheet="Summary")
        html = "<h1>Summary</h1>" + summary + "<br /><br /><h1>Output</h1>" + output
        html = html.replace('\\',  '\\\\')
        return html

    def update_confluence(self):
        confluence = Confluence(url=self.url, username=self.username, password=self.password)
        confluence.create_page(
            self.space, self.pageTitle, self.html, parent_id=self.rootPage, type='page', representation='storage'
        )

    def xlsx2html(self, filePath, sheet):
        wb = xlrd.open_workbook(filePath)
        sht = wb.sheet_by_name(sheet)
        data = []
        remove_index = []
        for row in range(sht.nrows):
            dt = []
            for column in range(sht.ncols):
                if row == 0:
                    if str(sht.cell_value(row, column)).lower() in self.remove_headers:
                        remove_index.append(column)
                    else:
                        dt.append(escape(str(sht.cell_value(row, column))))
                else:
                    if column not in remove_index:
                        dt.append(escape(str(sht.cell_value(row, column))))
            data.append('<td>' + '</td>\n<td>'.join(dt) + '</td>')
        html = '<table>' + '<tr>' + '</tr>\n<tr>'.join(data) + '</tr>' + '</table>'
        return html
