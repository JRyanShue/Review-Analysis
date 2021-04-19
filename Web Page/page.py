import json
import nltk
from flask import Flask
from wtforms import (Form, TextField, validators, SubmitField,
                     DecimalField, IntegerField)
from flask import render_template
from flask import request
import tensorflow
from nltk import word_tokenize
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np

# nltk.download('punkt')

app = Flask(__name__)


# Home page
# @app.route("/", methods=['GET', 'POST'])
# def home():
#     """Home page of app with form"""
#     # Create form
#     form = ReusableForm(request.form)
#
#     # Send templates information to index.html
#     return open("test.html").read()
@app.route('/login/', methods=['post', 'get'])
def login():
    message = ''
    if request.method == 'POST':
        review = request.form.get('review')  # access the data inside

        if review:
            message = "Your review:", review
        else:
            message = "No review entered"

        # load neural net
        model = tensorflow.keras.models.load_model("trained_model")

        # read in evidence to get dictionary
        with open("evidence.txt") as f:
            data = json.loads(f.read())

        # convert long string into sequence of indices

        tokenized_input = word_tokenize(review)
        dictionary_size = 5000  # top words to keep
        tokenizer = Tokenizer(num_words=dictionary_size)
        tokenizer.fit_on_texts(data)  # update vocabulary
        tokenized_input = tokenizer.texts_to_sequences(tokenized_input)  # encode tokenized evidence

        print(tokenized_input)

        model_input = []
        for item in tokenized_input:
            for i in item:
                model_input.append(i)

        # while len(model_input) < 50:
        #     model_input.append(0)

        model_input = [model_input]

        print("Predicting on:", model_input)

        # prediction = model.predict(tokenized_input, verbose=0)
        prediction_raw = model.predict(model_input, verbose=0)

        # determine how the prediction translates into stars
        stars_given = 0
        highest_predict_value = 0
        counter = 0
        for i in prediction_raw:
            for j in i:
                counter += 1
                if j > highest_predict_value:
                    stars_given = counter
                    highest_predict_value = j

        prediction = stars_given

        if prediction is not None:
            message = "Stars Given:", prediction

    return render_template('index.html', message=message)


app.run(host='0.0.0.0', port=5000)
