def cm_data_convert(cm_dataset):

    data_series = cm_dataset['series']
    data_list = []
    data_list_list = []
    for data in data_series:
        data_list.append(data['values'])

    for data_data in data_list:
        data_list_list.append(data_data[0])


    float_data = list(map(float, data_list_list))
    return float_data

  