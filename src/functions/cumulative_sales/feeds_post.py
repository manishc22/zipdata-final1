from dotenv import load_dotenv
from supabase import create_client, Client
import os
import streamlit as st

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


# @st.cache_data
def load_feed_posts(workspace):
    data = supabase.table('t_feed_post_tbl').select(
        "*").eq('workspace', workspace).execute()
    return data.data
