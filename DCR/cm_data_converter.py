import pandas as pd

def cm_date_format(cm_dataset):

    sup_series = cm_dataset['series']
    sup_list = []
    sup_sup_list = []
    
    for thing in sup_series:
        sup_list.append(thing['time'])
        df = pd.DataFrame(sup_list)
        
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
    
    df_1 = pd.DataFrame(float_data)
    
    return df_1

