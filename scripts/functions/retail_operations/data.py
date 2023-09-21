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
def monthly_store_data():
    m_store_data = supabase.table('monthly_store_perf').select(
        "*").execute()
    return m_store_data


@st.cache_data
def monthly_store_cumulative_data():
    m_retail_data = supabase.table('monthly_store_sales_perf').select(
        "*").execute()
    return m_retail_data


@st.cache_data
def monthly_store_growth_data():
    m_growth_data = supabase.table('monthly_store_growth_metrics').select(
        "*").execute()
    return m_growth_data


@st.cache_data
def quarterly_store_data():
    q_store_data = supabase.table('quarterly_store_perf').select(
        "*").execute()
    return q_store_data


@st.cache_data
def quarterly_store_cumulative_data():
    q_retail_data = supabase.table('quarterly_store_sales_perf').select(
        "*").execute()
    return q_retail_data


@st.cache_data
def quarterly_store_growth_data():
    q_growth_data = supabase.table('s_store_tbl').select(
        "q_value").eq('name', 'Cumulative').execute()
    return q_growth_data
