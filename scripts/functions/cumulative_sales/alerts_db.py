import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def alerts_insert(dataframe):
    print(dataframe['Workspace'][0])
    data_insert = supabase.table('t_alerts_setup_tbl').insert(
        {'workspace': dataframe['Workspace'][0], 'alert_name': dataframe['Alert Name'][0], 'alert_rule': dataframe['Alert Rule'][0],
         'status': dataframe['Status'][0]}).execute()
    return data_insert


def get_alerts(dataframe, workspace):
    data = supabase.table('t_alerts_setup_tbl').select(
        '*').eq('workspace', workspace).execute()
    df_alerts1 = pd.DataFrame.from_records(data.data)
    dataframe['ID'] = df_alerts1['id']
    dataframe['Workspace'] = df_alerts1['workspace']
    dataframe['Alert Name'] = df_alerts1['alert_name']
    dataframe['Alert Rule'] = df_alerts1['alert_rule']
    dataframe['Status'] = df_alerts1['status']
    return dataframe, df_alerts1


def update_alerts(dataframe):
    update_dict = {}
    for column in dataframe.columns.values:
        id = dataframe.loc['id', column]
        for ind in dataframe.loc[:, column].index:
            if ind != 'id' and dataframe.loc[ind, column] != '':
                update_dict[ind] = dataframe.loc[ind, column]
        update = supabase.table('t_alerts_setup_tbl').update(
            update_dict).eq('id', id).execute()
        update_dict = {}

    return update


def new_key(key):
    new_key = ''
    count = 0
    if key == 'Workspace':
        new_key = 'workspace'
        count = count + 1
    if key == 'Alert Name':
        new_key = 'alert_name'
        count = count + 1
    if key == 'Alert Rule':
        new_key = 'alert_rule'
        count = count + 1
    if key == 'Status':
        new_key = 'status'
        count = count + 1

    return new_key, count


def update_preprocess_alerts(dataframe, df_alerts1):
    # print(type(dataframe.loc['Delivery Time'].values[0]))
    for column in dataframe.columns.values:
        dataframe.loc['id', column] = df_alerts1.loc[column, 'id']
        dataframe.fillna('', inplace=True)
        for ind in dataframe.loc[:, column].index:
            var = dataframe.loc[ind, column]
            if var != '' and ind != 'id':
                new_key1, count = new_key(ind)
                # print(ind, new_key1)
                if count == 1:
                    dataframe.rename(index={ind: new_key1}, inplace=True)
    return dataframe
