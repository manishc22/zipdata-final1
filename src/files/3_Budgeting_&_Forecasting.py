from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
# data = supabase.table('quarterly_pl').select("*").execute()
# ratios = supabase.table('quarterly_ratios').select("*").execute()


# df = pd.DataFrame(data.data)
# df_ratios = pd.DataFrame(ratios.data)

st.set_page_config(layout='wide')
# col1, col2 = st.columns([1, 4])
# st.columns
tab1, tab2, tab3, tab4 = st.tabs(
    ['Revenue Forecasting', 'Expense Budgeting', 'Financial Modeling', 'Cash Flow Forecasting'])
