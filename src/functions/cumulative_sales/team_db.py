import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client
import os
import datetime

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def team_insert(dataframe):
    print(dataframe)
    data_insert = supabase.table('workspace_team').insert(
        {'workspace': dataframe['Workspace'][0], 'name': dataframe['Name'][0], 'email': dataframe['Email'][0],
         'is_admin': dataframe['Is Admin'][0], 'status': dataframe['Status'][0]}).execute()
    return data_insert


def get_team(dataframe):
    data = supabase.table('workspace_team').select('*').execute()
    df_team1 = pd.DataFrame.from_records(data.data)

    dataframe['ID'] = df_team1['id']
    dataframe['Workspace'] = df_team1['workspace']
    dataframe['Name'] = df_team1['name']
    dataframe['Email'] = df_team1['email']
    dataframe['Is Admin'] = df_team1['is_admin']
    dataframe['Status'] = df_team1['status']
    return dataframe, df_team1


def update_team(dataframe):
    update_dict = {}
    for column in dataframe.columns.values:
        id = dataframe.loc['id', column]
        for ind in dataframe.loc[:, column].index:
            if ind != 'id' and dataframe.loc[ind, column] != '':
                update_dict[ind] = dataframe.loc[ind, column]
        update = supabase.table('workspace_team').update(
            update_dict).eq('id', id).execute()
        update_dict = {}

    return update


def new_key(key):
    new_key = ''
    count = 0
    if key == 'Workspace':
        new_key = 'workspace'
        count = count + 1
    if key == 'Name':
        new_key = 'name'
        count = count + 1
    if key == 'Email':
        new_key = 'email'
        count = count + 1
    if key == 'Is Admin':
        new_key = 'is_admin'
        count = count + 1
    if key == 'Status':
        new_key = 'status'
        count = count + 1

    return new_key, count


def update_preprocess(dataframe, df_feeds1):

    for column in dataframe.columns.values:
        dataframe.loc['id', column] = df_feeds1.loc[column, 'id']
        dataframe.fillna('', inplace=True)
        for ind in dataframe.loc[:, column].index:
            var = dataframe.loc[ind, column]
            if var != '' and ind != 'id':
                new_key1, count = new_key(ind)
                # print(ind, new_key1)
                if count == 1:
                    dataframe.rename(index={ind: new_key1}, inplace=True)
    return dataframe
