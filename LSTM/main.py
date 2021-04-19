"""
takes in list of data and creates the model on it
"""

import json
import model


def convert_data(raw_list):
    obj_list = json.loads(raw_list)
    data_list = []
    # print(obj_list)
    for item in obj_list:
        # print("ITEM:", item)
        # print(type(item))
        try:
            data_list.append(json.loads(item))
            # print("added")
        except:
            print("exception occured.")
    return data_list


# load in data (JSON objects)
with open("LSTM/data.txt") as f:
    data = convert_data(f.read())

# create sets of evidence (summary) and labels (overall rating)
evidence = []
labels = []
for datapoint in data:
    evidence.append(datapoint["summary"])
    labels.append(datapoint["overall"])

# print(evidence)
# print(labels)

model.run(evidence, labels)

# convert_data()
