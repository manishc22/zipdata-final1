from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

load_dotenv()


@st.cache_resource
def load_supabase():
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase


supabase = load_supabase()

data = supabase.table('quarterly_pl').select("*").execute()
ratios = supabase.table('quarterly_ratios').select("*").execute()


df = pd.DataFrame(data.data)
df_ratios = pd.DataFrame(ratios.data)


funct = st.sidebar.radio(label="Choose an Option",
                         options=['Select a base', 'Plan & Model', 'Variance Analysis'])
df_empty = pd.DataFrame

if 'df' not in st.session_state or 'gross_margin' not in st.session_state or 'operating_margin' not in st.session_state:
    st.session_state['df'] = df_empty
    st.session_state['gross_margin'] = 0
    st.session_state['operating_margin'] = 0
    st.session_state['net_margin'] = 0
    st.session_state['term'] = ''
if funct == 'Select a base':

    with st.sidebar:
        st.divider()
        quarter = st.selectbox('*Term*', options=df['term'])
        st.session_state['df'] = df_empty
        st.session_state['gross_margin'] = 0
        st.session_state['operating_margin'] = 0
        st.session_state['net_margin'] = 0

    st.title('P & L Scenario Analysis')
    st.caption('*in million $*')
    st.divider()
    df1 = df[df['term'] == quarter].T.reset_index()
    # df_q_ratio = df_ratios[df_ratios['term'] == quarter]
    df1.columns = ['index', 'Value']
    df2 = df1.drop(df1.index[[1]])
    # df2.set_index("index", inplace=True)
    df2.loc[0, 'labels'] = 'Term'
    df2.loc[2, 'labels'] = 'Revenue'
    df2.loc[3, 'labels'] = 'Cost of Revenue'
    df2.loc[4, 'labels'] = 'Gross Profit'
    df2.loc[5, 'labels'] = 'R & D'
    df2.loc[6, 'labels'] = 'SG & A'
    df2.loc[7, 'labels'] = 'Restructuring Charges'
    df2.loc[8, 'labels'] = 'Total Operating Expenses'
    df2.loc[9, 'labels'] = 'Income from Operations'
    df2.loc[10, 'labels'] = 'Interest Income'
    df2.loc[11, 'labels'] = 'Interest Expense'
    df2.loc[12, 'labels'] = 'Other Income'
    df2.loc[13, 'labels'] = 'Total Other Income'
    df2.loc[14, 'labels'] = 'Income before Income Taxes'
    df2.loc[15, 'labels'] = 'Total Taxes'
    df2.loc[16, 'labels'] = 'Net Income'
    df2.set_index("labels", inplace=True)
    df3 = df2.drop(['index'], axis=1)
    st.session_state['df'] = df3
    st.session_state.gross_margin = round(
        df_ratios[df_ratios['term'] == quarter]['gross_margin']*100, 2)
    st.session_state.operating_margin = round(
        df_ratios[df_ratios['term'] == quarter]['operating_profit_margin']*100, 2)
    st.session_state.net_margin = round(
        df_ratios[df_ratios['term'] == quarter]['net_margin']*100, 2)
    # AgGrid(df2, width='100%')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label='**:blue[Gross Margin %]**',
                  value=round(df_ratios[df_ratios['term'] == quarter]['gross_margin']*100, 2))
    with col2:
        st.metric(label='**:blue[Operating Profit Margin %]**',
                  value=round(df_ratios[df_ratios['term'] == quarter]['operating_profit_margin']*100, 2))

    with col3:
        st.metric(label='**:blue[Net Margin %]**',
                  value=round(df_ratios[df_ratios['term'] == quarter]['net_margin']*100, 2))

    st.table(df3)

if funct == 'Plan & Model':
    print(st.session_state['gross_margin'])
    gross_margin = float(st.session_state['gross_margin'].values)
    operating_margin = float(st.session_state['operating_margin'].values)
    net_margin = float(st.session_state['net_margin'].values)
    df4 = st.session_state['df']
    int_income_pct = round(df4.loc['Interest Income',
                                   'Value'] * 100 / df4.loc['Revenue', 'Value'], 2)
    int_exp_pct = round(df4.loc['Interest Expense',
                                'Value'] * 100 / df4.loc['Revenue', 'Value'], 2)
    other_income_pct = round(df4.loc['Other Income',
                                     'Value'] * 100 / df4.loc['Revenue', 'Value'], 2)

    with st.sidebar:
        st.divider()
        if st.session_state.term:
            term_proj = st.text_input(
                '**Projected Term**', st.session_state.term)
        else:
            term_proj = st.text_input('**Projected Term**')

        st.session_state.term = term_proj
        revenue_new = float(df4.loc[df4.index[1]][0])

        rev_low = round(revenue_new - 0.5*revenue_new, 1)
        rev_high = round(revenue_new + 0.5*revenue_new, 1)
        step = round(revenue_new/100, 1)
        revenue_slider = st.slider(
            'Revenue', rev_low, rev_high, revenue_new, step=step)

        gross_margin_new = st.slider(
            "Gross Margin", 0.0, 100.0, gross_margin, step=0.25)
        operating_margin_new = st.slider(
            "Operating Margin", 0.0, 100.0, operating_margin, step=0.25)
        net_margin_new = st.slider(
            "Net Margin", 0.0, 100.0, net_margin, step=0.25)

    st.title('Modify Metrics to Plan for next Term')

    df4.loc['Term', 'Projections'] = term_proj
    df4.loc['Revenue', 'Projections'] = revenue_slider
    df4.loc['Gross Profit', 'Projections'] = round(
        gross_margin_new*revenue_slider/100, 1)
    df4.loc['Cost of Revenue', 'Projections'] = round(revenue_slider - (
        gross_margin_new*revenue_slider/100), 1)
    df4.loc['Income before Income Taxes', 'Projections'] = round(
        operating_margin_new*revenue_slider/100, 1)
    df4.loc['Net Income', 'Projections'] = round(
        net_margin_new*revenue_slider/100, 1)
    df4.loc['Total Taxes', 'Projections'] = round(
        ((operating_margin_new*revenue_slider/100) - (net_margin_new*revenue_slider/100)), 1)
    df4.loc['Interest Income', 'Projections'] = round(
        (int_income_pct*revenue_slider/100), 1)
    df4.loc['Interest Expense', 'Projections'] = round(
        (int_exp_pct*revenue_slider/100), 1)
    df4.loc['Other Income', 'Projections'] = round(
        (other_income_pct*revenue_slider/100), 1)
    df4.loc['Total Other Income', 'Projections'] = round((int_income_pct*revenue_slider/100) + (
        int_exp_pct*revenue_slider/100) + (other_income_pct*revenue_slider/100), 2)
    df4.loc['Income from Operations', 'Projections'] = round((int_income_pct*revenue_slider/100) + (
        int_exp_pct*revenue_slider/100) + (other_income_pct*revenue_slider/100) + (
        operating_margin_new*revenue_slider/100), 2)
    df4.loc['Total Operating Expenses', 'Projections'] = round(df4.loc['Gross Profit',
                                                                       'Projections'] - df4.loc['Income from Operations', 'Projections'], 2)

    rd_pct = round(df4.loc['R & D',
                           'Value'] / df4.loc['Total Operating Expenses', 'Value'], 3)
    sg_pct = round(df4.loc['SG & A',
                           'Value'] / df4.loc['Total Operating Expenses', 'Value'], 3)
    df4.loc['R & D', 'Projections'] = round(
        rd_pct*df4.loc['Total Operating Expenses', 'Projections'], 2)
    df4.loc['SG & A', 'Projections'] = round(
        sg_pct*df4.loc['Total Operating Expenses', 'Projections'], 2)
    df4.loc['Restructuring Charges', 'Projections'] = round(
        (1-(rd_pct+sg_pct))*df4.loc['Total Operating Expenses', 'Projections'], 2)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label='**:green[Gross Margin %]**',
                  value=gross_margin_new)

    with col2:
        st.metric(label='**:green[Operating Profit Margin %]**',
                  value=operating_margin_new)

    with col3:
        st.metric(label='**:green[Net Margin %]**',
                  value=net_margin_new)

    st.table(df4)
    st.button('Save and Upload')
