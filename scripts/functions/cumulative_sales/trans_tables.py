import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def trans_data(table):
    data = supabase.table(table).select(
        "*").limit(1000).execute()

    return data


def hide_columns(dataframe):

    # if 'month_id' in dataframe.columns:
    #     dataframe.drop(columns=['month_id'], inplace=True)

    if 'id' in dataframe.columns:
        dataframe.drop(columns=['id'], inplace=True)

    if 'created_at' in dataframe.columns:
        dataframe.drop(columns=['created_at'], inplace=True)

    return dataframe


def get_months(dataframe):
    dataframe_new = dataframe[['month_id', 'month_name']].drop_duplicates()
    dataframe_new.sort_values('month_id', inplace=True)
    return dataframe_new
