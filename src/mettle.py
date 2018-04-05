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
        # self.email = self.config_email()
        # self.model_loader = ModelMethods()

    def config_db(self):
        return {
            "apiKey": "AIzaSyCsWK-fZ8sQIg3ReJjderS58_b_hZSNjmg",
            "authDomain": "mlticket-6a2a8.firebaseapp.com",
            "databaseURL": "https://mlticket-6a2a8.firebaseio.com",
            "storageBucket": "",
        }

    def autheticate(self):
        """
        Handles authentication and connection to firebaseDB
        """
        self.firebase = pyrebase.initialize_app(self.config_db())
        self.auth = self.firebase.auth()
        user = self.auth.sign_in_with_email_and_password(self.config.db_email, self.config.db_pwd)
        self.db = self.firebase.database()
        return self.db

    def add(self, folder, data):
        key = self.db.child(folder).push(data)
        return key

    def update(self, folder, data):
        self.db.child(folder).update(data)

    def listen(self):
        self.listener = self.db.child("tickets").stream(
            stream_handler=self.stream_handler,
        )

    def stream_handler(self, message):
        info = list(message['data'].keys())[0].split('/')
        type = info[-1]
        id = info[0]
        # if type == "actual" or type == "category":
        #     pass
        if type == "resolved":
            data = id.val()
            print(data)
            self.add("archive", id + "/")
            self.db.child("tickets").remove(id)
        else:
            classification = self.classify(message)
            self.update("tickets", {id + "/prediction": classification})
            return

    def process_message(self, ticket):
        pass


if __name__ == "__main__":
    mettle = Mettle()
