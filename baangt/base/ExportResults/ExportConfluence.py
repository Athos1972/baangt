from xlsx2html import xlsx2html
from bs4 import BeautifulSoup as bs
from atlassian import Confluence


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
        self.update_confluence()

    def makeBody(self):
        output_html = self.makeOutput()
        summary_html = self.makeSummary()
        html = "<h1>Summary</h1>" + summary_html + "<br /><br /><h1>Output</h1>" + output_html
        html = html.replace('\\',  '\\\\')
        return html

    def makeOutput(self):
        output = xlsx2html(self.fileNameAndPathToResultXLSX, sheet="Output")
        output.seek(0)
        output_soup = bs(output.read(), "html.parser")
        output_text = output_soup.find("table")
        output_text.attrs = {}
        tr = output_text.find("tr")
        td = tr.find_all("td")
        json_index = []
        for x in range(len(td)):
            if td[x].text.strip().lower() in self.remove_headers:
                json_index.append(x)
        json_index.sort(reverse=True)
        for index in json_index:
            td[index].decompose()
        trs = output_text.find_all("tr")[1:]
        for index in json_index:
            for tds in trs:
                td = tds.find_all("td")
                td[index].decompose()
        for tag in output_text():
            tag.attrs = {}  # remove all attributes from html
        return str(output_text)

    def makeSummary(self):
        summary = xlsx2html(self.fileNameAndPathToResultXLSX, sheet="Summary")
        summary.seek(0)
        summary_text = bs(summary.read(), "html.parser").find("table")
        summary_text.attrs = {}
        for tag in summary_text():
            tag.attrs = {}
        return str(summary_text)

    def update_confluence(self):
        confluence = Confluence(url=self.url, username=self.username, password=self.password)
        confluence.create_page(
            self.space, self.pageTitle, self.html, parent_id=self.rootPage, type='page', representation='storage'
        )
