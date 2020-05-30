import requests
import xlrd
import json
import hashlib
import logging


logger = logging.getLogger('pyC')


class SendMail:
    def __init__(self, settings, filename):
        self.globalSettings = settings
        self.filename = filename
        self.attachment = self.globalSettings.get("NotificationWithAttachment")
        self.url = "https://mgw.baangt.org"
        self.create_body()
        self.prepare_json()
        self.generate_files()
        self.send_mail()

    def create_body(self):
        """
        Will create body from mail by using summary tab of xlsx output file.
        Any changes in body structure should be made in this function.
        :return:
        """
        wb = xlrd.open_workbook(self.filename)
        sheet = wb.sheet_by_name("Summary")
        data = []
        for x in range(2, sheet.nrows):
            lis = []
            for cell in sheet.row(x):
                value = cell.value
                if type(value) == float:
                    value = str(value)
                    if value[-2:] == '.0':
                        value = value[:-2]
                else:
                    value = str(value).strip()
                lis.append(value)
            while "" in lis:
                lis.remove("")
            if lis != []:
                data.append(' = '.join(lis))
        self.subject = sheet.row(0)[0].value.strip()
        self.body = '\n'.join(data)

    def prepare_json(self):
        """Will create json file which we will send in request"""
        recipientList = self.globalSettings.get("SendMailTo")
        recipientList = recipientList.split(',')
        recipientList = [emails.strip() for emails in recipientList]
        dic = {
            'recipientList': recipientList,
            'subject': self.subject,
            'body': self.body,
        }
        self.json_data = self.prepare_csm(dic)

    def prepare_csm(self, dic):
        """Create checksum and add it in json"""
        json_string = json.dumps(dic)
        csm = hashlib.md5(json_string.encode('utf-8')).hexdigest()
        dic['csm'] = csm
        json_data = json.dumps(dic)
        return json_data

    def generate_files(self):
        """Create Files parameter for request, will send json along with xlsx(attachment) file"""
        if self.attachment == "True" or self.attachment is True:
            self.files = {'xlsx': (self.filename,
                              open(self.filename, 'rb'),
                              'application/vnd.ms-excel', {'Expires': '0'}),
                     'json': ('json', self.json_data, 'application/json')}
        else:
            self.files = {'json': ('json', self.json_data, 'application/json')}

    def send_mail(self):
        """Will make the post request to mail gateway"""
        logger.info("Sending mails...")
        try:
            res = requests.post(self.url, files=self.files)
        except Exception as ex:
            logger.debug(ex)
            return None
        response = json.loads(res.content.decode('utf-8'))
        for mail in response:
            logger.info(f"{mail} = {response[mail]}")
