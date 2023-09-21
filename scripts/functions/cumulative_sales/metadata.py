import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client
import os
from sqlalchemy import create_engine, text, URL


load_dotenv()


@st.cache_resource
def sql_engine():
    engine = create_engine(
        "postgresql://postgres:o6m7DUBhhoMvYaTJ@db.attmalwrbocsfvwbkmur.supabase.co:6543/postgres")
    return engine


@st.cache_data
def trans_metadata(workspace):
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from workspace_access_tbl 
               where table_type = 'BASE TABLE' and workspace = :workspace
               """)
        data = pd.read_sql_query(
            sql, conn, params={"workspace": workspace})
    return data


@st.cache_data
def views_metadata(workspace):
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from workspace_access_tbl 
               where table_type = 'VIEW' and workspace = :workspace
               """)
        data = pd.read_sql_query(
            sql, conn, params={"workspace": workspace})
    return data


def get_quarters(quarter):
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from o_quarters_tbl where id > 
            (select id from o_quarters_tbl where label = :quarter) order by id asc limit 4
               """)
        data = pd.read_sql_query(
            sql, conn, params={"quarter": quarter})
    return data


def target_months(month_name):
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from o_months_tbl where id >
            (select id from o_months_tbl where month_name = :month_name) order by id asc limit 3
               """)
        data = pd.read_sql_query(
            sql, conn, params={"month_name": month_name})
    return data
