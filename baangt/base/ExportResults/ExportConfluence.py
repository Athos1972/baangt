from atlassian import Confluence
from html import escape
import xlrd
import os


class ExportConfluence:
    def __init__(self, url, space, pageTitle, fileNameAndPathToResultXLSX, username, password, rootPage=None,
                 remove_headers=["json"], uploadOriginalFile=False, CreateSubPagesForEachXXEntries=0):
        self.url = url
        self.space = space
        self.rootPage = rootPage
        self.pageTitle = pageTitle
        self.fileNameAndPathToResultXLSX = fileNameAndPathToResultXLSX
        self.username = username
        self.password = password
        self.remove_headers = [headers.lower() for headers in remove_headers]
        self.uploadOriginalFile = uploadOriginalFile
        self.CreateSubPagesForEachXXEntries = CreateSubPagesForEachXXEntries
        self.html = self.makeBody()
        self.update_confluence()

    def makeBody(self):
        summary = self.xlsx2html(self.fileNameAndPathToResultXLSX, sheet="Summary")
        if not self.CreateSubPagesForEachXXEntries:
            output = self.xlsx2html(self.fileNameAndPathToResultXLSX, sheet="Output")
            html = "<h1>Summary</h1>" + summary + "<br /><br /><h1>Output</h1>" + output
        else:
            html = "<h1>Summary</h1>" + summary + "<br />"
        html = html.replace('\\',  '\\\\')
        return html

    def update_confluence(self):
        confluence = Confluence(url=self.url, username=self.username, password=self.password)  # Confluence login
        if self.uploadOriginalFile:
            file = self.attach_file(confluence)
            html = file + "<br /><br />" + self.html
        else:
            html = self.html
        new_page = confluence.create_page(
            self.space, self.pageTitle, html, parent_id=self.rootPage, type='page', representation='storage'
        )
        if self.CreateSubPagesForEachXXEntries:
            try:
                parent_page = new_page["id"]
            except KeyError:
                parent_page = new_page["results"]["id"]




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
        try:
            url = "/confluence"+attach["_links"]["download"].split(".xlsx?")[0] + ".xlsx"
        except KeyError:
            url = "/confluence"+attach["results"][0]["_links"]["download"].split(".xlsx?")[0] + ".xlsx"
        link = f'<a href="{url}">{fileName}</a>'
        html = "<h1>Original file</h1>"+link
        return html

    def create_child_pages(self, confluence, parent_page):
        wb = xlrd.open_workbook(self.fileNameAndPathToResultXLSX)
        output_xlsx = wb.sheet_by_name("Output")
        starting_points = [x for x in range(1, output_xlsx.nrows, self.CreateSubPagesForEachXXEntries)]
        header = []
        remove_index = []
        for x in range(output_xlsx.ncols):
            value = output_xlsx.cell_value(0, x)
            if value.lower() not in self.remove_headers:
                header.append(value)
            else:
                remove_index.append(x)
        header = '<tr><th>' + '</th>\n<th>'.join(header) + '</th></tr>'
        for starting in starting_points:
            if starting + self.CreateSubPagesForEachXXEntries < output_xlsx.nrows:
                ending = starting + self.CreateSubPagesForEachXXEntries
            else:
                ending = output_xlsx.nrows
            title = ((len(str(output_xlsx.nrows)) - len(str(starting))) * "0") + str(starting
                    ) + " - " + ((len(str(output_xlsx.nrows)) - len(str(ending))) * "0") + str(ending)
            data = []
            for row in range(starting, ending):
                dt = []
                for column in range(output_xlsx.ncols):
                    value = output_xlsx.cell_value(row, column)
                    if type(value) == float:
                        if repr(value)[-2:] == '.0':
                            value = int(value)
                    value = str(value)
                    if column not in remove_index:  # if column is not in remove_header list than add the data in html
                        dt.append(escape(value))
                data.append('<td>' + '</td>\n<td>'.join(dt) + '</td>')
            html = '<table><tbody>' + header + '<tr>' + '</tr>\n<tr>'.join(data) + '</tr>' + '</tbody></table>'
            confluence.create_page(
                self.space, title, html, parent_id=parent_page, type='page', representation='storage'
            )

