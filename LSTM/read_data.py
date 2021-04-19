import json

"""
This file is responsible for formatting the given json into a list and then saving it
"""


def separate_objects(raw):
    """
    The dataset I'm using is not formatted correctly, so this function splits objects into a list (not done so already)
    :param raw:
    :return:
    """
    data_to_parse = raw  # shortens over time as data is parsed away
    obj_list = []

    index = 0
    while True:
        # print(index)
        # print(len(data_to_parse))
        if data_to_parse[index] == "}" and data_to_parse[index + 1] is not None:
            obj_list.append(data_to_parse[:index + 1])  # put object into list
            print("Data added:", data_to_parse[:index + 1])
            data_to_parse = data_to_parse[index + 1:]
            index = 0
        # check to see if finished
        if len(data_to_parse) < 2000:  # don't check before a certain point (efficiency)
            # if only one { and only one }, only one object left to parse
            if data_to_parse.count("{") == 1 and data_to_parse.count("}") == 1:
                obj_list.append(data_to_parse)
                break
        index += 1
        # print("loop")

    return obj_list


def load_data(file_path):
    with open(file_path) as f:
        raw_data = f.read()
        print(type(raw_data))
        print(raw_data[0])
        print(raw_data[393])
        print("x")
        raw_data.replace(""
                         "", "")
        # print("RAW:", raw_data)
        raw_list = separate_objects(raw_data)
        with open('../data.txt', 'w') as file:
            json.dump(raw_list, file)

        # d = json.load(f)
        # print(d)

    # file = open(file_path, )
    # data = json.load(file)

    # save object list for future training
    # with open('data.txt', 'w') as file:
    #     json.dump(obj_list, file)

