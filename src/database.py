import pyrebase


class Database:
    def __init__(self):
        self.db = self.autheticate()
        self.firebase = None
        self.auth = None
        self.listener = None

    def stream_handler(self, message):
        print(message)
        path = message['data']
        type = list(path.keys())[0].split('/')[-1]
        print(type)
        if type == "actual":
            print("") # divert to uupdate ticket in place
        else:
            pass

    def config(self):
        return {
            "apiKey": "AIzaSyCsWK-fZ8sQIg3ReJjderS58_b_hZSNjmg",
            "authDomain": "mlticket-6a2a8.firebaseapp.com",
            "databaseURL": "https://mlticket-6a2a8.firebaseio.com",
            "storageBucket": "",
        }

    def autheticate(self):
        self.firebase = pyrebase.initialize_app(self.config())
        self.auth = self.firebase.auth()
        user = self.auth.sign_in_with_email_and_password('hgrace503@gmail.com', 'hello30')
        print(user["localId"])
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
    database = Database()
    database.add({""})
    database.listen()
