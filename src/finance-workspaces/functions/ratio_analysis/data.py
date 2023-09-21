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
def quarterly_ratios():
    data = supabase.table('quarterly_ratios').select(
        "*").execute()
    return data
