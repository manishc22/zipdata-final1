from supabase import create_client, Client
import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()


def load_supabase():
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase


supabase = load_supabase()


@st.cache_data
def monthly_state_product_data():
    data = supabase.table('a_dim_value_tbl').select(
        "value").eq('analysis_id', 16).execute()
    return data


@st.cache_data
def monthly_growth_product_data():
    data = supabase.table('a_dim_value_tbl').select(
        "value").eq('analysis_id', 15).execute()
    return data


@st.cache_data
def quarterly_state_product_data():
    data = supabase.table('a_dim_value_tbl').select(
        "value").eq('analysis_id', 18).execute()
    return data


@st.cache_data
def quarterly_growth_product_data():
    data = supabase.table('a_dim_value_tbl').select(
        "value").eq('analysis_id', 19).execute()
    return data
