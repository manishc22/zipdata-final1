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


def hide_columns(dataframe_raw):

    if 'month_id' in dataframe_raw.columns:
        dataframe = dataframe_raw.drop(columns=['month_id'])

    if 'id' in dataframe_raw.columns:
        dataframe = dataframe_raw.drop(columns=['id'])

    if 'created_at' in dataframe.columns:
        dataframe = dataframe_raw.drop(columns=['created_at'])

    return dataframe


def get_months(dataframe):
    dataframe_new = dataframe[['month_id', 'month_name']].drop_duplicates()
    dataframe_new.sort_values('month_id', inplace=True)
    return dataframe_new
