import keras


class model_methods:
    def __init__(self):
        self.deepdive_model = keras.models.load_model('model1.h5')

    def get_prediction(self, input):
        # This method takes in an input of an array of strings and outputs a prediction
        test = self.deepdive_model.predict(input)
        print(test)

test = model_methods()
test