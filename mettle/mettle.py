"""
Mettle
@version 1.0
@author Ben Ong, Grace Han
@created 02/04/18
@modified 05/01/18
"""

import pyrebase
import string
import re
from mettle_config import MettleConfig
from model_loader import ModelMethods
from pyfiglet import figlet_format


class Mettle:

    def __init__(self):
        self.config = MettleConfig()
        self.db = self.authenticate()
        self.firebase = None
        self.auth = None
        self.listener = self.listen()
        self.model_loader = ModelMethods()

    def welcome(self):
        """
        sweet backend UI
        """
        print(figlet_format('welcome to mettle', font='speed'))
        print('version 2.4.1 by Ben Ong, Dan Xie, Grace Han')

    def authenticate(self):
        """
        Handles authentication and connection to firebase
        """
        self.firebase = pyrebase.initialize_app(self.config.config_db())
        self.auth = self.firebase.auth()
        user = self.auth.sign_in_with_email_and_password(self.config.db_email, self.config.db_pwd)
        self.db = self.firebase.database()
        self.welcome()
        # data = self.config.db_schema()
        # results = self.db.child("users").push(data, user['idToken'])
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
        # print(message)
        # print(message)
        try:
            info = list(message['data'].keys())[0].split('/')
            type = info[-1]
            id = info[0]
            id2 = message['path']

            # ticket resolved: archive ticket
            if type == "resolved":
                data = self.db.child("tickets").child(id2).get()
                data = data.val()
                self.add("archive", data)
                self.db.child("tickets").child(id2).remove()

            # classification was manually updated, increment
            # if type == "actual":
                # data = self.db.child("tickets").child(id).get()
                # new_category = data["actual"]

            # ticket sent to NN to be classified
            else:
                try:
                    message_str = message['data']['desc']
                    message_str_clean = self.process_message(message_str)
                    classification = self.model_loader.classify(message_str_clean)
                    self.db.child("tickets").child(id2).update({'prediction': classification[0]})
                    self.db.child("tickets").child(id2).update({'prediction': classification[0]})
                    self.db.child("tickets").child(id2).update({'confidence': float(classification[1])})
                    delimiter = "----------------------------------"
                    print("\nID:{}\nMessage: {}\nPredicted Category: {}\nPrediction Confidence: {}\n{}".format
                          (id2[2:], message_str, str(classification[0]), str(classification[1]), delimiter))
                except KeyError:
                    pass
        except AttributeError as a:
            pass
        # except KeyError as e:
        #     print(e)
        #     pass


    # def output(self, case):
    #     delimiter = "----------------------------------"
    #     if case == "resolve":
    #         print("\n{}\nID:{}\nMessage: {}\nPredicted Category: {}\nPrediction Confidence: {}\n{}".format)
    #     if case == "add":
    #
    #     if case == "man_update":


    def process_message(self, message):
        dirty = message
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
        delimiter = "----------------------------------"
        print("{}\nMessage: {}\nCleaned Message: {}".format(delimiter, dirty, message))

        return message


if __name__ == "__main__":
    mettle = Mettle()
