import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


class ModelMethods:
    def __init__(self):
        self.vocab_size = 1500
        self.embedding_size = 100
        self.seq_len = 15
        self.categories = 7
        self.deepdive_model = keras.models.load_model('rnn.h5')

    def condition_data(self, data):
        print(data)
        tokenizer = Tokenizer(num_words=self.vocab_size - 1, oov_token=None)
        tokenizer.fit_on_texts(data)
        # tokenizer.texts_to_sequences(data)
        print(data)
        x = pad_sequences(tokenizer.texts_to_sequences([data]), maxlen=self.seq_len)
        print(x)
        input('')
        return x

    def classify(self, data):
        final_data = self.condition_data(data)
        print(final_data)

        # This method takes in an input of an array of strings and outputs a prediction
        return self.deepdive_model.predict(final_data)


test = ModelMethods()
test.classify('my access account inquiry')
