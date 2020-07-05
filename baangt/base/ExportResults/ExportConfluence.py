from xlsx2html import xlsx2html
from bs4 import BeautifulSoup as bs
from atlassian import Confluence


class ExportConfluence:
    def __init__(self, url, space, pageTitle, fileNameAndPathToResultXLSX, username, password, rootPage=None):
        self.url = url
        self.space = space
        self.rootPage = rootPage
        self.pageTitle = pageTitle
        self.fileNameAndPathToResultXLSX = fileNameAndPathToResultXLSX
        self.username = username
        self.password = password
        self.html = self.makeBody()
        self.update_confluence()

    def makeBody(self):
        output_html = self.makeOutput()
        summary_html = self.makeSummary()
        html = "<h1>Summary</h1>" + summary_html + "<br><br><h1>Output</h1>" + output_html
        return html

    def makeOutput(self):
        output = xlsx2html(self.fileNameAndPathToResultXLSX, sheet="Output")
        output.seek(0)
        output_soup = bs(output.read(), "html.parser")
        output_text = output_soup.find("table")
        output_text["border"] = 1
        tr = output_text.find("tr")
        td = tr.find_all("td")
        json_index = None
        for x in range(len(td)):
            if td[x].text.strip().lower() == "json":
                json_index = x
                td[x].decompose()
        trs = output_text.find_all("tr")[1:]
        if json_index is not None:
            for tds in trs:
                td = tds.find_all("td")
                td[json_index].decompose()
        for tag in output_text():
            tag.attrs = {}  # remove all attributes from html
        output_html = str(output_text).replace("", "")
        return output_html

    def makeSummary(self):
        summary = xlsx2html(self.fileNameAndPathToResultXLSX, sheet="Summary")
        summary.seek(0)
        summary_text = bs(summary.read(), "html.parser").find("table")
        summary_text["border"] = 1
        for tag in summary_text():
            tag.attrs = {}
        summary_html = str(summary_text).replace("", "")
        return summary_html

    def update_confluence(self):
        confluence = Confluence(url=self.url, username=self.username, password=self.password)
        confluence.create_page(
            self.space, self.pageTitle, self.html, parent_id=self.rootPage, type='page', representation='storage'
        )
