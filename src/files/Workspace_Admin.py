from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
import datapane as dp
import streamlit.components.v1 as components
import datetime
from functions import trans_tables
from functions import metadata

st.set_page_config(layout='wide')
now = datetime.date.today()
load_dotenv()
dp.login(token="8a6aa6da0365af22aa8b58e103a9532e12af9dc3")


url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


@st.cache_data
def analysis_data():
    data = supabase.table('a_dim_value_tbl').select(
        "*").execute()
    return data


@st.cache_data
def analysis_seed():
    data = supabase.table('a_analysis_tbl').select(
        "*").execute()
    return data


metadata = metadata.metadata()
print(metadata)
analysis_master = analysis_data().data
df_analysis_master = pd.DataFrame.from_records(analysis_master)

analysis_sd = analysis_seed().data
df_analysis_seed = pd.DataFrame.from_records(analysis_sd)

st.write('#### Workspace Admin')
st.caption(
    'Integrated, single-window, view of all your Workspaces')
st.markdown('   ')
col20, col21, col22 = st.columns(3, gap='large')
with col20:
    st.selectbox('*Select a Workspace*', options=['Performance Dashboards',
                 'Financial Reporting & Analytics', 'Financial Ops & Control'])

st.markdown('   ')
tab1, tab2, tab3 = st.tabs(['Data Hub', 'Feeds', 'Team'])

with tab1:
    col1, col2, col3, col4, col5 = st.columns([1.5, 4, 2, 0.75, 0.75])
    with col1:
        option = st.selectbox('*Select Data Type*', options=[
            'Transactional', 'Analysis', 'Forecasts', 'Recommendations'])

    if option == 'Transactional':
        df_tables = trans_tables.transaction_tables()
        min_date = datetime.datetime.strptime('01-01-2020', '%m-%d-%Y').date()
        date_value = now.replace(day=1)
        with col3:
            table_label = st.selectbox(
                '*Tables*', options=df_tables['label'])
            table_name = df_tables[df_tables['label']
                                   == table_label]['table'].values[0]
            df_table_data = pd.DataFrame(
                trans_tables.trans_data(table_name).data)

        with col4:
            start_dt = st.date_input(
                "*Enter Start Date*", min_value=min_date, max_value=now, value=date_value)

        with col5:
            end_dt = st.date_input(
                "*Enter End Date*", min_value=start_dt, max_value=now)

        description = table_label
        st.divider()
        col8, col9, col10 = st.columns([1, 5, 1])
        with col9:
            with st.expander(f"**{description}**: *Custom Rules & Queries*"):
                st.write('Query 1')

        if df_table_data.shape[0] > 0:
            v = dp.DataTable(df_table_data)

            html = dp.stringify_report(v)
            components.html(html, height=600, width=None, scrolling=False)
    if option == 'Analysis':
        with col3:
            analysis_type = st.selectbox(
                '*Report Category*', options=df_analysis_seed[df_analysis_seed['published'] == True]['analysis_type'])
            analysis_id = df_analysis_seed[df_analysis_seed['analysis_type']
                                           == analysis_type]['id']

        with col4:
            term = st.selectbox(
                '*Term*', options=df_analysis_master[df_analysis_master['analysis_id'] == analysis_id.values[0]]['term'])

        title = df_analysis_seed[df_analysis_seed['analysis_type']
                                 == analysis_type]['analysis_type'].values[0]

        description = df_analysis_seed[df_analysis_seed['analysis_type']
                                       == analysis_type]['description'].values[0]
        value_df = df_analysis_master[(df_analysis_master['term'] == term) & (
            df_analysis_master['analysis_id'] == analysis_id.values[0])]['value']

        df_analysis = pd.DataFrame.from_records(
            value_df[value_df.index.values[0]])

        if 'index' in df_analysis.columns:
            df_analysis.drop(columns=['index'], inplace=True, axis=1)

        # # if df_analysis.shape[0] < df_analysis.shape[1]:
        # #     df_analysis = df_analysis.T

        st.divider()

        col8, col9 = st.columns([3, 2])
        with col8:
            with st.expander(f"**{description}**: *Custom Rules & Queries*"):
                st.write('Query 1')

        v = dp.DataTable(df_analysis)

        html = dp.stringify_report(v)
        components.html(html, height=600, width=None, scrolling=False)

with tab2:
    st.markdown('###### Define Alerts')
