import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
from tensorflow import get_default_graph


class ModelMethods:
    def __init__(self):
        self.vocab_size = 2000
        self.embedding_size = 100
        self.seq_len = 15
        self.categories = 7

        # Load the deepdive cnn model
        self.deepdive_model = keras.models.load_model('../models/deepdive-cnn2.h5')
        self.graph = get_default_graph()
        # Unpickle our tokenizer
        with open('../models/tokenizer.pkl', 'rb') as f:
            self.tokenizer = pickle.load(f)

    @staticmethod
    def lookup_table(argument):
        d = {
            0: 'Access Issues / Security Enablement',
            1: 'Application',
            2: 'H/W',
            3: 'Job Failures',
            4: 'N/W',
            5: 'S/W',
        }
        return d[argument]

    def condition_data(self, data):
        # tokenizer.texts_to_sequences(data)
        # print(data)
        x = pad_sequences(self.tokenizer.texts_to_sequences([data]), maxlen=self.seq_len)
        return x

    def classify(self, data):
        final_data = self.condition_data(data)
        with self.graph.as_default():
            # This method takes in an input of an array of strings and outputs a prediction
            output = self.deepdive_model.predict(final_data)[0]
        output_max = np.argmax(output)
        confidence = output[output_max]

        # We are returning (string, confidence)
        return self.lookup_table(output_max + 1), confidence


if __name__ == '__main__':
    test = ModelMethods()
    hello = test.classify('my access account inquiry')
    print(hello)
