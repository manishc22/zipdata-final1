import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def targets_insert(dataframe):

    data_insert = supabase.table('t_targets_setup_tbl').insert(
        {'workspace': dataframe['Workspace'][0], 'target_name': dataframe['Target Name'][0], 'term': dataframe['Term'][0], 'target_rule': dataframe['Target Rule'][0],
         'update_frequency': dataframe['Update Frequency'][0], 'delivery_time': dataframe['Delivery Time'][0], 'status': dataframe['Status'][0]}).execute()
    return data_insert


def get_targets(dataframe, workspace):
    data = supabase.table('t_targets_setup_tbl').select(
        '*').eq('workspace', workspace).execute()
    df_targets1 = pd.DataFrame.from_records(data.data)
    df_targets1['delivery_time'] = pd.to_datetime(
        df_targets1['delivery_time'], format='%H:%M:%S')
    dataframe['ID'] = df_targets1['id']
    dataframe['Workspace'] = df_targets1['workspace']
    dataframe['Target Name'] = df_targets1['target_name']
    dataframe['Term'] = df_targets1['term']
    dataframe['Target Rule'] = df_targets1['target_rule']
    dataframe['Update Frequency'] = df_targets1['update_frequency']
    dataframe['Delivery Time'] = df_targets1['delivery_time']
    dataframe['Status'] = df_targets1['status']
    return dataframe, df_targets1


def update_targets(dataframe):
    update_dict = {}
    for column in dataframe.columns.values:
        id = dataframe.loc['id', column]
        for ind in dataframe.loc[:, column].index:
            if ind != 'id' and dataframe.loc[ind, column] != '':
                update_dict[ind] = dataframe.loc[ind, column]
        update = supabase.table('t_targets_setup_tbl').update(
            update_dict).eq('id', id).execute()
        update_dict = {}

    return update


def new_key(key):
    new_key = ''
    count = 0
    if key == 'Workspace':
        new_key = 'workspace'
        count = count + 1
    if key == 'Target Name':
        new_key = 'target_name'
        count = count + 1
    if key == 'Term':
        new_key = 'term'
        count = count + 1
    if key == 'Target Rule':
        new_key = 'target_rule'
        count = count + 1
    if key == 'Update Frequency':
        new_key = 'update_frequency'
        count = count + 1
    if key == 'Delivery Time':
        new_key = 'delivery_time'
        count = count + 1
    if key == 'Status':
        new_key = 'status'
        count = count + 1

    return new_key, count


def update_preprocess_targets(dataframe, df_targets1):
    # print(type(dataframe.loc['Delivery Time'].values[0]))
    for column in dataframe.columns.values:
        dataframe.loc['id', column] = df_targets1.loc[column, 'id']
        dataframe.fillna('', inplace=True)
        for ind in dataframe.loc[:, column].index:
            var = dataframe.loc[ind, column]
            if var != '' and ind != 'id':
                new_key1, count = new_key(ind)
                # print(ind, new_key1)
                if count == 1:
                    dataframe.rename(index={ind: new_key1}, inplace=True)
    return dataframe
