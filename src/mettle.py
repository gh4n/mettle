import pyrebase
import smtplib
import time
import imaplib
import email
from mettle_config import MettleConfig
from model_loader import ModelMethods


class Mettle:

    def __init__(self):
        self.config = MettleConfig()
        self.db = self.autheticate()
        self.firebase = None
        self.auth = None
        self.listener = self.listen()
        self.model_loader = ModelMethods()

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
        print(message)
        try:
            info = list(message['data'].keys())[0].split('/')
            type = info[-1]
            id = info[0]
            message_str = message['data']['desc']

            if type == "resolved":
                data = self.db.child("tickets").child(id).get()
                data = data.val()
                self.add("archive", data)
                self.db.child("tickets").child(id).remove()
            else:
                print("hello")
                classification = self.model_loader.classify(message_str)
                print(classification)
                self.update("tickets", {id + "/prediction" : classification[0]})
                self.update("tickets", {id + "/confidence": classification[1]})
                return
        except AttributeError as e:
            print(e)
            pass
        except KeyError as e:
            print(e)
            pass

    def process_message(self, ticket):
        pass


if __name__ == "__main__":
    mettle = Mettle()


