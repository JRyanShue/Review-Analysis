"""
Neural network model
"""
import json

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import random
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.layers import Embedding
from nltk import word_tokenize
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.layers import LSTM
from tensorflow.keras.layers import Dense

TEST_SIZE = 0.2

# hyperparameter: number of training samples to work through before the model’s internal parameters are updated
BATCH_SIZE = 64

BUFFER_SIZE = 10000


def run(evidence, labels):

    # convert long strings of evidence into sequences of indices
    tokenized_evidence = []  # tokenize
    for item in evidence:
        tokenized_evidence.append(word_tokenize(item))

    # with open('evidence.txt', 'w') as file:  # save tokenized evidence
    #     json.dump(tokenized_evidence, file)
    # while True:
    #     print("done")

    # print("TE:", tokenized_evidence)
    dictionary_size = 5000  # top words to keep
    tokenizer = Tokenizer(num_words=dictionary_size)
    tokenizer.fit_on_texts(tokenized_evidence)  # update vocabulary
    # print("CONFIG:", tokenizer.get_config())
    tokenized_evidence = tokenizer.texts_to_sequences(tokenized_evidence)  # encode tokenized evidence
    # print("X:", tokenized_evidence)

    # convert labels into usable format
    for item_no in range(len(labels)):
        labels[item_no] = int(labels[item_no])
    nd_labels = np.array(labels)
    # One hot encoding (only 5 different values)
    encoder = OneHotEncoder(sparse=False)
    nd_labels = nd_labels.reshape(-1, 1)
    processed_labels = encoder.fit_transform(nd_labels)
    # for i in range(len(processed_labels)):
    #     print("PROCESSED_LABELS:", processed_labels[i], end=";")
    #     print("ORIGINAL_LABEL:", nd_labels[i])

    # split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(
        tokenized_evidence, processed_labels, test_size=TEST_SIZE
    )

    # pad data and truncate reviews that are longer than given length
    max_review_length = 50
    x_train = sequence.pad_sequences(x_train, maxlen=max_review_length)
    x_test = sequence.pad_sequences(x_test, maxlen=max_review_length)

    # create the model
    embedding_vector_length = 32
    model = tf.keras.Sequential()
    model.add(Embedding(dictionary_size, embedding_vector_length, input_length=max_review_length))
    model.add(LSTM(100))
    model.add(Dense(5, activation='sigmoid'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=3, batch_size=64)

    # Final evaluation of the model
    scores = model.evaluate(x_test, y_test, verbose=0)
    print("Accuracy: %.2f%%" % (scores[1] * 100))

    model.save("trained_model", save_format='h5')
