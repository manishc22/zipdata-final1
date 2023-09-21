from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
import datapane as dp
import streamlit.components.v1 as components

load_dotenv()
dp.login(token="8a6aa6da0365af22aa8b58e103a9532e12af9dc3")

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

st.set_page_config(layout='wide')

tab1, tab2 = st.tabs(
    ['Plan & Model', 'Variance Analysis'])


with tab1:
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

    analysis_master = analysis_data().data
    df_analysis_master = pd.DataFrame.from_records(analysis_master)

    analysis_sd = analysis_seed().data
    df_analysis_seed = pd.DataFrame.from_records(analysis_sd)

    col1, col2, col3, col4 = st.columns([1, 1, 2, 1], gap='large')
    with col1:

        analysis_type = st.selectbox(
            '*Report Category*', options=df_analysis_seed[df_analysis_seed['published'] == True]['analysis_type'])
        analysis_id = df_analysis_seed[df_analysis_seed['analysis_type']
                                       == analysis_type]['id']

    with col2:
        term = st.selectbox(
            '*Term*', options=df_analysis_master[df_analysis_master['analysis_id'] == analysis_id.values[0]]['term'])

    st.divider()

    title = df_analysis_seed[df_analysis_seed['analysis_type']
                             == analysis_type]['analysis_type'].values[0]

    description = df_analysis_seed[df_analysis_seed['analysis_type']
                                   == analysis_type]['description'].values[0]

    value_df = df_analysis_master[(df_analysis_master['term'] == term) & (
        df_analysis_master['analysis_id'] == analysis_id.values[0])]['value']

    df_analysis = pd.DataFrame.from_records(
        value_df[value_df.index.values[0]])

    df_projection = pd.DataFrame(columns=['Metrics', 'Targets'])
    df_projection['Metrics'] = df_analysis.columns
    el_m = [x for x in df_analysis.columns if x == "month_id"]
    el_mn = [x for x in df_analysis.columns if x == "month_name"]
    el_in = [x for x in df_analysis.columns if x == "index"]
    el_col = [x for x in df_analysis.columns if x == "col_id"]
    el_q = [x for x in df_analysis.columns if x == "quarter_id"]
    el_qn = [x for x in df_analysis.columns if x == "quarter"]

    if el_q:
        df_projection.drop(
            df_projection[df_projection.Metrics == 'quarter_id'].index[0], inplace=True, axis=0)

    if el_qn:
        df_projection.drop(
            df_projection[df_projection.Metrics == 'quarter'].index[0], inplace=True, axis=0)

    if el_col:
        df_projection.drop(
            df_projection[df_projection.Metrics == 'col_id'].index[0], inplace=True, axis=0)
    if el_m:
        df_projection.drop(
            df_projection[df_projection.Metrics == 'month_id'].index[0], inplace=True, axis=0)

    if el_in:
        df_projection.drop(
            df_projection[df_projection.Metrics == 'index'].index[0], inplace=True, axis=0)

    if el_mn:
        df_projection.drop(
            df_projection[df_projection.Metrics == 'month_name'].index[0], inplace=True, axis=0)

    if df_analysis.shape[0] < df_analysis.shape[1]:
        df_analysis = df_analysis.T

    col5, col6 = st.columns([2, 1.5], gap='large')
    with col5:
        st.write(
            f"###### Select baseline Data: *{description}*")
        st.markdown("   ")
        st.data_editor(df_analysis, hide_index=True, height=None,
                       width=None, use_container_width=True, column_config={'index': None, 'month_id': None})

        with col6:

            col8, col9 = st.columns(2)

            with col8:
                term_projected = st.text_input(
                    '**Projected Term**', value='Set Targets for Projected Term', label_visibility='collapsed')
            st.data_editor(df_projection, hide_index=True, height=None,
                           width=None, use_container_width=True, disabled=("Index"))
            with col9:
                st.button('Save and Upload')

with tab2:
    st.write('#### Modify Metrics to Plan for next Term')
    # print(st.session_state['gross_margin'])
