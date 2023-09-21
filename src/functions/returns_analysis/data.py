from supabase import create_client, Client
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()


def load_supabase():
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase


supabase = load_supabase()


@st.cache_data
def monthly_online_returns_data():
    data = supabase.table('a_dim_value_tbl').select(
        "value").eq('analysis_id', 20).execute()
    return data


@st.cache_data
def monthly_retail_returns_data():
    data = supabase.table('a_dim_value_tbl').select(
        "value").eq('analysis_id', 21).execute()
    return data


@st.cache_data
def monthly_state_returns_data():
    data = supabase.table('a_dim_value_tbl').select(
        "value").eq('analysis_id', 22).execute()
    return data


@st.cache_data
def monthly_product_returns_data():
    data = supabase.table('a_dim_value_tbl').select(
        "value").eq('analysis_id', 23).execute()
    return data
