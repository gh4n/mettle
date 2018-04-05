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
            id2 = message['path']

            # ticket resolved: archive ticket
            if type == "resolved":
                data = self.db.child("tickets").child(id).get()
                data = data.val()
                self.add("archive", data)
                self.db.child("tickets").child(id).remove()

            # classifcation was manually updated, increment
            if type == "actual":
                data = self.db.child("tickets").child(id).get()
                new_category = data["actual"]
                self.incr_corrected(new_category)

            # ticket sent to NN to be classified
            else:
                classification = self.model_loader.classify(message_str)
                print(classification)
                self.db.child("tickets").child(id2).update({'prediction': classification[0]})
                self.db.child("tickets").child(id2).update({'confidence':float(classification[1])})
                print('im updating to the id', id2)
                self.incr_aggr(classification[0])
                return
        except AttributeError as e:
            print(e)
            pass
        except KeyError as e:
            print(e)
            pass

    def incr_aggr(self, category):
        na = self.db.child("analytics").child("aggregate_all").get()
        na += 1
        self.db.child("analytics").child("aggregate_all").update(na)

        na_category = self.db.child("analytics").child("category_all").child(category).get()
        na_category += 1
        self.db.child("analytics").child("category_all").child(category).update(na_category)

        return

    def incr_corrected(self, category):
        nc = self.db.child("analytics").child("aggregate_corrected").get()
        nc += 1
        self.db.child("analytics").child("aggregate_corrected").update(nc)

        nc_category = self.db.child("analytics").child("category_corrected").child(category).get()
        nc_category += 1
        self.db.child("analytics").child("category_corrected").child(category).update(nc_category)
        return


if __name__ == "__main__":
    mettle = Mettle()


