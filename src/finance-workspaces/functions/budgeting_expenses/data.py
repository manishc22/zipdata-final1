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
def monthly_total_expenses():
    data = supabase.table('a_dim_value_tbl').select(
        "value").eq('analysis_id', 24).execute()
    return data


@st.cache_data
def monthly_category_expenses():
    data = supabase.table('a_dim_value_tbl').select(
        "value").eq('analysis_id', 25).execute()
    return data
