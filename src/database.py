import pyrebase
import abc
# from model_loader import ModelMethods()


class Mettle:
    def __init__(self):
        self.db = self.autheticate()
        self.firebase = None
        self.auth = None
        self.listener = None
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
            print(id)

    def config(self):
        return {
            "apiKey": "AIzaSyCsWK-fZ8sQIg3ReJjderS58_b_hZSNjmg",
            "authDomain": "mlticket-6a2a8.firebaseapp.com",
            "databaseURL": "https://mlticket-6a2a8.firebaseio.com",
            "storageBucket": "",
        }

    def read_emails(self):
        return

    def autheticate(self):
        self.firebase = pyrebase.initialize_app(self.config())
        self.auth = self.firebase.auth()
        user = self.auth.sign_in_with_email_and_password('hgrace503@gmail.com', 'hello30')
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


if __name__ == "__main__":
    database = Mettle()
    database.add({""})
    database.listen()
