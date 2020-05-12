def cm_date_format(cm_dataset):

    sup_series = cm_dataset['series']
    sup_list = []
    sup_sup_list = []
    
    for thing in sup_series:
        sup_list.append(thing['time'])

    for item in sup_list:
        #new_item = parser.parse(item)
        new_item = pd.to_datetime(item)
        sup_sup_list.append(new_item)

    df = pd.DataFrame(sup_sup_list)

    return df

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

