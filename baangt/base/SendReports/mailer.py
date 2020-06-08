import requests
import os
import json
import hashlib
import logging


logger = logging.getLogger('pyC')


class SendMail:
    def __init__(self, settings, filename, subject, body, attach_file=""):
        self.globalSettings = settings
        self.filename = filename
        if attach_file == "":
            self.attach_file = filename
        else:
            self.attach_file = attach_file
        self.attachment = self.globalSettings.get("NotificationWithAttachment")
        self.url = "https://mgw.baangt.org"
        self.subject = subject
        self.body = body
        self.prepare_json()
        self.generate_files()
        self.send_mail()


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
        if os.path.exists(self.attach_file):
            if self.attachment == "True" or self.attachment is True:
                self.files = {'xlsx': (self.attach_file,
                                  open(self.attach_file, 'rb'),
                                  'application/vnd.ms-excel', {'Expires': '0'}),
                        'json': ('json', self.json_data, 'application/json')}
                print(f"sending {self.attach_file}")
            else:
                print("no attachment")
                self.files = {'json': ('json', self.json_data, 'application/json')}
        else:
            logger.info(f"File not exist {self.attach_file}")
            self.files = {'json': ('json', self.json_data, 'application/json')}

    def send_mail(self):
        """Will make the post request to mail gateway"""
        logger.info("Sending mails...")
        try:
            res = requests.post(self.url, files=self.files)
        except Exception as ex:
            logger.debug(ex)
            return None
        try:
            response = json.loads(res.content.decode('utf-8'))
            for mail in response:
                logger.info(f"{mail} = {response[mail]}")
        except:
            logger.info(res.content.decode('utf-8'))
