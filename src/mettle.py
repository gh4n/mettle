import pyrebase
import smtplib
import time
import imaplib
import email
from mettle_config import MettleConfig
# from model_loader import ModelMethods()


class Mettle:

    def __init__(self):
        self.config = MettleConfig()
        self.db = self.autheticate()
        self.firebase = None
        self.auth = None
        self.listener = None
        self.email = self.config_email()
        # self.model_loader = ModelMethods()

    def stream_handler(self, message):
        info = list(message['data'].keys())[0].split('/')
        type = info[-1]
        id = info[0]
        if type == "actual" or type == "category":
            pass
        else:
            classification = self.classify(message)
            self.update({id + "/prediction" : classification})

    def config_db(self):
        return {
            "apiKey": "AIzaSyCsWK-fZ8sQIg3ReJjderS58_b_hZSNjmg",
            "authDomain": "mlticket-6a2a8.firebaseapp.com",
            "databaseURL": "https://mlticket-6a2a8.firebaseio.com",
            "storageBucket": "",
        }

    def config_email(self):
        config = EmailConfig()
        mail = imaplib.IMAP4_SSL(config.STMP_SERVER)
        mail.login(config.FROM_EMAIL, config.FROM_PWD)
        mail.select('inbox')
        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()
        latest_email_id = int(id_list[-1])
        type, data = mail.fetch(str.encode(str(latest_email_id)), '(RFC822)')

        for response in data:
            if isinstance(response, tuple):
                msg = email.message_from_string(response[1].decode())
                email_subject = msg['subject']
                email_from = msg['from']
                for message_data in msg.getpayload():
                    print(message_data)
        return

    def read_emails(self):
        return

    def autheticate(self):
        self.firebase = pyrebase.initialize_app(self.config_db())
        self.auth = self.firebase.auth()
        # HIDE THIS LINE LMAO
        user = self.auth.sign_in_with_email_and_password(self.config.db_pwd, self.config.db_pwd)
        self.db = self.firebase.database()
        return self.db

    def add(self, data):
        key = self.db.child("tickets").push(data)
        return key

    def update(self, data):
        self.db.child("tickets").update(data)

    def listen(self):
        self.listener = self.db.child("tickets").stream(
            stream_handler=self.stream_handler,
        )

    def process(self, ticket):
        pass


if __name__ == "__main__":
    mettle = Mettle()


