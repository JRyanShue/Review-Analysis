"""
Neural network model
"""
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split


def run(evidence, labels):
    # create list of (evidence, label) pairs
    data_pairs = []
    for i in range(len(evidence)):
        data_pairs.append(tuple(evidence[i], labels[i]))

    # split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(evidence, labels, test_size=0.2, random_state=42)

    print("running")
