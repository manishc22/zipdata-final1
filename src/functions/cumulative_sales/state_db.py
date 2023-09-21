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
def load_monthly_data():
    data = supabase.table('monthly_state_performance').select(
        "*").execute()
    return data


@st.cache_data
def load_growth_data():
    growth_data = supabase.table('monthly_sales_growth').select(
        "*").execute()
    return growth_data


@st.cache_data
def load_quarterly_data():
    quarterly_data = supabase.table('quarterly_state_performance1').select(
        "*").execute()
    return quarterly_data


@st.cache_data
def load_yearly_data():
    yearly_data = supabase.table('s_states_tbl').select(
        "y_value").eq('name', 'Cumulative').execute()
    return yearly_data


@st.cache_data
def load_state_ranks():
    state_ranks = supabase.table('state_ranks').select(
        "*").execute()
    return state_ranks


@st.cache_data
def quarterly_state_ranks():
    q_state_ranks = supabase.table('q_state_ranks').select(
        "*").execute()
    return q_state_ranks
