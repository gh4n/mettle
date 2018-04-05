import pyrebase
import string
import re
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

    def autheticate(self):
        """
        Handles authentication and connection to firebaseDB
        """
        self.firebase = pyrebase.initialize_app(self.config.config_db())
        self.auth = self.firebase.auth()
        user = self.auth.sign_in_with_email_and_password(self.config.db_email, self.config.db_pwd)
        self.db = self.firebase.database()
        print("WELCOME")
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
                # self.incr_corrected(new_category)

            # ticket sent to NN to be classified
            else:
                message_str = self.process_message(message_str)
                print(message_str)
                classification = self.model_loader.classify(message_str)
                self.db.child("tickets").child(id2).update({'prediction': classification[0]})
                self.db.child("tickets").child(id2).update({'prediction': classification[0]})
                self.db.child("tickets").child(id2).update({'confidence':float(classification[1])})
                print('im updating to the id', id2)
                # self.incr_aggr(classification[0])
                return
        except AttributeError as e:
            print(e)
            pass
        except KeyError as e:
            print(e)
            pass


    def process_message(self, message):
        regex = re.compile('[%s]' % re.escape(string.punctuation))
        # replace newlines
        message = regex.sub('', message)
        # remove punctuation
        message = message.replace('/n', ' ')
        # replace strings of numbers with generic NUM
        message = re.sub(r'[0-9]{3}\w+', ' NUM', message)
        # cull unnecessary whitespaces
        message = re.sub(r' +', ' ', message)
        # lowercase
        message = message.lower()
        return message

    def incr_aggr(self, category):
        na = self.db.child("analytics").child("aggregate_all").get().val()
        print(na)
        na += 1
        self.db.child("analytics").update({"aggregate_all":na})

        na_category = self.db.child("analytics").child("category_all").child(category).get().val()
        na_category += 1
        self.db.child("analytics").child("category_all").update({category:na_category})
        return

    def incr_corrected(self, category):
        nc = self.db.child("analytics").child("aggregate_corrected").get().val()
        nc += 1
        self.db.child("analytics").child("aggregate_corrected").update(nc)

        nc_category = self.db.child("analytics").child("category_corrected").child(category).get().val
        nc_category += 1
        self.db.child("analytics").child("category_corrected").child(category).update(nc_category)
        return


if __name__ == "__main__":
    mettle = Mettle()


