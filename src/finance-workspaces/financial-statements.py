import streamlit.components.v1 as components
import datetime as dt
from datetime import date, time
import datapane as dp
import altair as alt
import pandas as pd
import streamlit as st

from functions.financial_statements import data
from functions.utilities.trans_tables import *
from functions.utilities.feeds_post import *
from functions.utilities.metadata import *
from functions.utilities.targets_db import *
from functions.utilities.alerts_db import *

st.set_page_config(
    page_title="Financial Statements Analysis",
    layout="wide"
)


q_pl = data.quarterly_pl().data
df_q_pl = pd.DataFrame.from_records(q_pl)

q_bs = data.quarterly_bs().data
df_q_bs = pd.DataFrame.from_records(q_bs)

tab1, tab2, tab3, tab4 = st.tabs(
    ['P&L Trends', 'BS Trends', 'Data Hub', 'Feeds'])

with tab1:
    col1, col2, col3, col4 = st.columns([1.25, 3, 1, 1.25])

    with col1:
        option_tab2 = st.selectbox('Select a View', options=['P&L Statements',
                                                             'P&L - Trends'], key='tab2-views')

    st.divider()
    if option_tab2 == 'P&L Statements':
        with col3:
            quarter = st.selectbox(
                'Select Quarter', options=df_q_pl['term'], key='tab2')
            # col8, col9, col10, col11 = st.columns(4, gap='large')
        st.markdown('##### Quarterly - P&L')
        df1 = df_q_pl[df_q_pl['term'] == quarter].T.reset_index()
    # df_q_ratio = df_ratios[df_ratios['term'] == quarter]
        df1.columns = ['index', 'Value']
        df2 = df1.drop(df1.index[[1]])
        # df2.set_index("index", inplace=True)
        df2.loc[0, 'Labels'] = 'Term'
        df2.loc[2, 'Labels'] = 'Revenue'
        df2.loc[3, 'Labels'] = 'Cost of Revenue'
        df2.loc[4, 'Labels'] = 'Gross Profit'
        df2.loc[5, 'Labels'] = 'R & D'
        df2.loc[6, 'Labels'] = 'SG & A'
        df2.loc[7, 'Labels'] = 'Restructuring Charges'
        df2.loc[8, 'Labels'] = 'Total Operating Expenses'
        df2.loc[9, 'Labels'] = 'Income from Operations'
        df2.loc[10, 'Labels'] = 'Interest Income'
        df2.loc[11, 'Labels'] = 'Interest Expense'
        df2.loc[12, 'Labels'] = 'Other Income'
        df2.loc[13, 'Labels'] = 'Total Other Income'
        df2.loc[14, 'Labels'] = 'Income before Income Taxes'
        df2.loc[15, 'Labels'] = 'Total Taxes'
        df2.loc[16, 'Labels'] = 'Net Income'
        df2.set_index("Labels", inplace=True)
        df3 = df2.drop(['index'], axis=1)
        col1, col2, col3 = st.columns([1, 2, 1], gap='large')
        with col2:
            st.dataframe(df3, height=598, width=400)

    if option_tab2 == 'P&L - Trends':
        st.markdown('##### Quarterly - P&L Trends')
        col1, col2 = st.columns(2, gap='large')
        with col1:

            chart1 = alt.Chart(df_q_pl, title='Revenue Trends').mark_bar().encode(
                x=alt.X('term', sort=None,
                        title='Quarters'),
                y=alt.Y('revenue', title='Revenue (in million)'
                        ),
            ).interactive()
            st.altair_chart(chart1,  use_container_width=True)

            chart3 = alt.Chart(df_q_pl, title='Gross Profit Trends').mark_line().encode(
                x=alt.X('term', sort=None,
                        title='Quarters'),
                y=alt.Y('gross_profit', title='Gross Profit (in million)'
                        ),
            ).interactive()
            st.altair_chart(chart3, use_container_width=True)

            chart5 = alt.Chart(df_q_pl, title='Net Income Trends').mark_line().encode(
                x=alt.X('term', sort=None,
                        title='Quarters'),
                y=alt.Y('net_income', title='Gross Profit (in million)'
                        ),
            ).interactive()
            st.altair_chart(chart5, use_container_width=True)

        with col2:
            chart2 = alt.Chart(df_q_pl, title='Cost of Revenue Trends').mark_line().encode(
                x=alt.X('term', sort=None,
                        title='Quarters'),
                y=alt.Y('cost_of_revenue',
                        title='Cost of Revenue (in million USD)'),
            ).interactive()
            st.altair_chart(chart2,  use_container_width=True)

            chart4 = alt.Chart(df_q_pl, title='Total Operating Expense Trends').mark_line().encode(
                x=alt.X('term', sort=None,
                        title='Quarters'),
                y=alt.Y('total_op_expenses', title='Total Operating Expenses (in million)'
                        ),
            ).interactive()
            st.altair_chart(chart4, use_container_width=True)

with tab2:
    col1, col2, col3, col4 = st.columns([1.25, 3, 1, 1.25])

    with col1:
        option_tab3 = st.selectbox('Select a View', options=['Balance Sheet',
                                                             'BS - Trends'], key='tab3-views')

    st.divider()
    if option_tab3 == 'Balance Sheet':
        with col3:
            quarter = st.selectbox(
                'Select Quarter', options=df_q_pl['term'], key='tab3')
           # col8, col9, col10, col11 = st.columns(4, gap='large')
        st.markdown('##### Quarterly - Balance Sheet (millions)')
        df1 = df_q_bs[df_q_bs['term'] == quarter].T.reset_index()
        df1.columns = ['index', 'Value']
        df2 = df1.drop(df1.index[[1]])

        df2.loc[0, 'Labels'] = 'Term'
        df2.loc[2, 'Labels'] = 'Assets'
        df2.loc[3, 'Labels'] = 'Cash & Cash Equivalents'
        df2.loc[4, 'Labels'] = 'Marketable Securities'
        df2.loc[5, 'Labels'] = 'Accounts Receivable'
        df2.loc[6, 'Labels'] = 'Inventories'
        df2.loc[7, 'Labels'] = 'Prepaid Expenses'
        df2.loc[8, 'Labels'] = 'Deferred Income Taxes'
        df2.loc[9, 'Labels'] = 'Total Current Assets'
        df2.loc[10, 'Labels'] = 'Property & Equipment'
        df2.loc[11, 'Labels'] = 'Goodwill'
        df2.loc[12, 'Labels'] = 'Intangible Assets'
        df2.loc[13, 'Labels'] = 'Other Assets'
        df2.loc[14, 'Labels'] = 'Total Assets'
        df2.loc[15, 'Labels'] = 'Liabilities'
        df2.loc[16, 'Labels'] = 'Accounts Payable'
        df2.loc[17, 'Labels'] = 'Accrued Current Liabilities'
        df2.loc[18, 'Labels'] = 'Convertible Short Term Debt'
        df2.loc[19, 'Labels'] = 'Total Current Liabilities'
        df2.loc[20, 'Labels'] = 'Total Long Term Debt'
        df2.loc[21, 'Labels'] = 'Other Liabilities'
        df2.loc[22, 'Labels'] = 'Capital Lease'
        df2.loc[23, 'Labels'] = 'Total Liabilities'
        df2.loc[24, 'Labels'] = 'Commitments & Contingencies'
        df2.loc[25, 'Labels'] = 'Convertible Debt Conversion'
        df2.loc[26, 'Labels'] = 'Preferred Stock'
        df2.loc[27, 'Labels'] = 'Common Stock'
        df2.loc[28, 'Labels'] = 'Paid in Capital'
        df2.loc[29, 'Labels'] = 'Treasury Stock'
        df2.loc[30, 'Labels'] = 'Accumulated other comprehensive loss'
        df2.loc[31, 'Labels'] = 'Retained Earnings'
        df2.loc[32, 'Labels'] = 'Total Shareholder Equity'
        df2.loc[33, 'Labels'] = 'Total liabilities, convertible debt & shareholders equity'

        df2.set_index("Labels", inplace=True)
        df3 = df2.drop(['index'], axis=1)
        col1, col2, col3 = st.columns([1, 2, 1], gap='large')
        with col2:
            st.dataframe(df3, height=1200, width=600)

    if option_tab3 == 'BS - Trends':
        st.markdown('##### Quarterly - BS Trends')
        col1, col2 = st.columns(2, gap='large')
        with col1:

            chart1 = alt.Chart(df_q_bs, title='Cash & Cash Equivalents Trends').mark_bar().encode(
                x=alt.X('term', sort=None,
                        title='Quarters'),
                y=alt.Y('cash_cash_equivalents', title='Cash (in million)'
                        ),
            )
            st.altair_chart(chart1,  use_container_width=True)

            chart3 = alt.Chart(df_q_bs, title='AR / AP Trends').mark_line(color='green').encode(
                x=alt.X('term', sort=None,
                        title='Quarters'),
                y=alt.Y('accounts_receivable', title='AR / AP'
                        ),
            )

            chart3_1 = alt.Chart(df_q_bs, title='AR / AP Trends').mark_line().encode(
                x=alt.X('term', sort=None,
                        title='Quarters'),
                y=alt.Y('accounts_payable',
                        ),
            )

            st.altair_chart(chart3 + chart3_1, use_container_width=True)

            chart5 = alt.Chart(df_q_bs, title='Total Inventory').mark_line().encode(
                x=alt.X('term', sort=None,
                        title='Quarters'),
                y=alt.Y('inventories', title='Total Inventory'
                        ),
            )
            st.altair_chart(chart5,  use_container_width=True)

        with col2:
            chart2 = alt.Chart(df_q_bs, title='Total Current Assets').mark_line().encode(
                x=alt.X('term', sort=None,
                        title='Quarters'),
                y=alt.Y('total_current_assets',
                        title='Total Current Assets (in million USD)'),
            ).interactive()
            st.altair_chart(chart2,  use_container_width=True)

            chart4 = alt.Chart(df_q_bs, title='Total Current Liabilities').mark_line().encode(
                x=alt.X('term', sort=None,
                        title='Quarters'),
                y=alt.Y('total_current_liab',
                        title='Current Liabilities (in million USD)'),
            ).interactive()
            st.altair_chart(chart4,  use_container_width=True)

            chart6 = alt.Chart(df_q_bs, title='Long Term Debt').mark_line().encode(
                x=alt.X('term', sort=None,
                        title='Quarters'),
                y=alt.Y('long_term_debt',
                        title='Long Term Debt'),
            )
            st.altair_chart(chart6,  use_container_width=True)
