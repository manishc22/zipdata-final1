import streamlit.components.v1 as components
import datetime as dt
from datetime import date, time

import altair as alt
import pandas as pd
import streamlit as st
from functions.returns_analysis import data
from functions.cumulative_sales.trans_tables import *
from functions.cumulative_sales.feeds_post import *
from functions.cumulative_sales.metadata import *
from functions.cumulative_sales.targets_db import *
from functions.cumulative_sales.alerts_db import *
from functions.cumulative_sales.state_db import *

st.set_page_config(
    page_title="Returns Analysis",
    layout="wide",
    initial_sidebar_state='collapsed'
)
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(
    ['Dashboard', 'Data Hub', 'Feeds'])


m_or_data = data.monthly_online_returns_data().data
df_m_or_data = pd.DataFrame.from_records(
    m_or_data[0]['value']).sort_values(by='month_id')
# df_m_or_data['transaction_dt'] = datetime.datetime.fromtimestamp(
#     df_m_or_data['transaction_dt']/1000)
# df_m_or_data['return_dt'] = datetime.datetime.fromtimestamp(
#     df_m_or_data['return_dt']/1000)

m_rr_data = data.monthly_retail_returns_data().data
df_m_rr_data = pd.DataFrame.from_records(
    m_rr_data[0]['value'])

m_sr_data = data.monthly_state_returns_data().data
df_m_sr_data = pd.DataFrame.from_records(
    m_sr_data[0]['value'])
df_m_sr_data['total_returns'] = df_m_sr_data['online_returns'] + \
    df_m_sr_data['retail_returns']

m_pr_data = data.monthly_product_returns_data().data
df_m_pr_data = pd.DataFrame.from_records(
    m_pr_data[0]['value'])

data = load_monthly_data()
df = pd.DataFrame(data.data).dropna(axis=0).sort_values(
    by=['month_id'], ascending=False)

months = df_m_or_data['month_name'].drop_duplicates()
col1, col2, col3, col4 = st.columns([1.75, 0.75, 1, 1.25], gap='large')
with col1:
    funct_tab4 = st.radio(label="Select a Term",
                          options=['Monthly', 'Quarterly', 'Yearly'], horizontal=True, key='tab4-term')

with col4:
    option_tab4 = st.selectbox('Select a Product Category', options=['Cumulative',
                                                                     '1 Seater Sofas', '2 Seater Sofas', '3 Seater Sofas'], key='tab4-views')
st.divider()

if funct_tab4 == 'Monthly' and option_tab4 == 'Cumulative':
    st.markdown('##### Monthly Returns - Cumulative Metrics')
    st.markdown(' ')
    with col2:
        month = st.selectbox(
            'Select Month', options=df_m_or_data['month_name'].drop_duplicates())

    col8, col9, col10 = st.columns(3, gap='large')
    with col8:
        total_returns = df_m_or_data[(df_m_or_data['month_name'] == month)]['order_id'].count(
        ) + df_m_rr_data[(df_m_rr_data['month_name'] == month)]['order_id'].count()

        st.metric(label='**:blue[Total Returns (Volume)]**',
                  value=total_returns)

        total_returns_pct = round(
            total_returns * 100 / (df[df['month_name'] == month]['online_orders'].sum() + df[df['month_name'] == month]['retail_orders'].sum()), 2)
        st.metric(label='**:blue[Total Returns %]**',
                  value=total_returns_pct)

        st.divider()
        df3 = df_m_sr_data[(df_m_sr_data['month_name'] == month)].sort_values(
            by='total_returns', ascending=False).head(10)

        chart = alt.Chart(df3, title='Top 10 States by Total Returns').mark_bar().encode(
            x=alt.X('state', sort=None, title='States'),
            y=alt.Y('total_returns',
                    title='Total Returns'),
        )
        st.altair_chart(chart,  use_container_width=True)
        # st.data_editor(
        #     df_m_sr_data[df_m_sr_data['month_name'] == month], hide_index=True)

    with col9:
        st.metric(label='**:blue[Total Online Returns (Volume)]**',
                  value=df_m_or_data[(df_m_or_data['month_name'] == month)]['order_id'].count(
                  ))
        returns_online = round(df_m_or_data[(df_m_or_data['month_name'] == month)]['order_id'].count(
        ) * 100 / (df[df['month_name'] == month]['online_orders'].sum()), 2)
        st.metric(label='**:blue[Total Returns Online %]**',
                  value=returns_online)
        st.divider()
        df4 = df_m_sr_data[(df_m_sr_data['month_name'] == month)].sort_values(
            by='online_returns', ascending=False).head(10)

        chart = alt.Chart(df4, title='Top 10 States by Online Returns').mark_bar().encode(
            x=alt.X('state', sort=None, title='States'),
            y=alt.Y('online_returns',
                    title='Online Returns'),
        )
        st.altair_chart(chart,  use_container_width=True)

    with col10:
        st.metric(label='**:blue[Total Returns Retail (Volume)]**',
                  value=df_m_rr_data[(df_m_rr_data['month_name'] == month)]['order_id'].count(
                  ))
        returns_retail = round(df_m_rr_data[(df_m_rr_data['month_name'] == month)]['order_id'].count(
        ) * 100 / (df[df['month_name'] == month]['retail_orders'].sum()), 2)

        st.metric(label='**:blue[Total Returns Retail %]**',
                  value=returns_retail)

        st.divider()
        df5 = df_m_sr_data[(df_m_sr_data['month_name'] == month)].sort_values(
            by='retail_returns', ascending=False).head(10)

        chart = alt.Chart(df5, title='Top 10 States by Retail Returns').mark_bar().encode(
            x=alt.X('state', sort=None, title='States'),
            y=alt.Y('retail_returns',
                    title='Retail Returns'),
        )
        st.altair_chart(chart,  use_container_width=True)
else:
    st.markdown(f'##### Monthly Returns for - {option_tab4}')
    st.markdown(' ')
    with col2:
        month = st.selectbox(
            'Select Month', options=df_m_or_data['month_name'].drop_duplicates())

    col8, col9, col10 = st.columns(3, gap='large')
    with col8:
        total_returns_p = df_m_or_data[(df_m_or_data['month_name'] == month) & (df_m_or_data['product_type'] == option_tab4)]['order_id'].count(
        ) + df_m_rr_data[(df_m_rr_data['month_name'] == month) & (df_m_rr_data['product_type'] == option_tab4)]['order_id'].count()

        st.metric(label=f'**:blue[Total Returns for {option_tab4} (Volume)]**',
                  value=total_returns_p)

        total_returns_pct = round(
            total_returns_p * 100 / (df[df['month_name'] == month]['online_orders'].sum() + df[df['month_name'] == month]['retail_orders'].sum()), 2)
        st.metric(label='**:blue[Total Returns %]**',
                  value=total_returns_pct)

        st.divider()
        df3 = df_m_pr_data[(df_m_pr_data['month_name'] == month) & (df_m_pr_data['product_type'] == option_tab4)].sort_values(
            by='total_returns', ascending=False).head(10)

        chart = alt.Chart(df3, title=f'Top 10 States by Total Returns of {option_tab4}').mark_bar().encode(
            x=alt.X('state', sort=None, title='States'),
            y=alt.Y('total_returns',
                    title='Total Returns'),
        )
        st.altair_chart(chart,  use_container_width=True)
        # st.data_editor(
        #     df_m_sr_data[df_m_sr_data['month_name'] == month], hide_index=True)

    with col9:
        st.metric(label=f'**:blue[Total Online Returns of {option_tab4}]**',
                  value=df_m_or_data[(df_m_or_data['month_name'] == month) & (df_m_or_data['product_type'] == option_tab4)]['order_id'].count(
                  ))
        returns_online = round(df_m_or_data[(df_m_or_data['month_name'] == month) & (df_m_or_data['product_type'] == option_tab4)]['order_id'].count(
        ) * 100 / (df[df['month_name'] == month]['online_orders'].sum()), 2)
        st.metric(label='**:blue[Total Returns Online %]**',
                  value=returns_online)
        st.divider()
        df4 = df_m_pr_data[(df_m_pr_data['month_name'] == month) & (df_m_pr_data['product_type'] == option_tab4)].sort_values(
            by='online_returns', ascending=False).head(10)

        chart = alt.Chart(df4, title='Top 10 States by Online Returns').mark_bar().encode(
            x=alt.X('state', sort=None, title='States'),
            y=alt.Y('online_returns',
                    title='Online Returns'),
        )
        st.altair_chart(chart,  use_container_width=True)

    with col10:
        st.metric(label=f'**:blue[Total Retail Returns of {option_tab4}]**',
                  value=df_m_rr_data[(df_m_rr_data['month_name'] == month) & (df_m_rr_data['product_type'] == option_tab4)]['order_id'].count(
                  ))
        returns_retail = round(df_m_rr_data[(df_m_rr_data['month_name'] == month) & (df_m_rr_data['product_type'] == option_tab4)]['order_id'].count(
        ) * 100 / (df[df['month_name'] == month]['retail_orders'].sum()), 2)

        st.metric(label='**:blue[Total Returns Retail %]**',
                  value=returns_retail)

        st.divider()
        df5 = df_m_pr_data[(df_m_pr_data['month_name'] == month) & (df_m_pr_data['product_type'] == option_tab4)].sort_values(
            by='retail_returns', ascending=False).head(10)

        chart = alt.Chart(df5, title='Top 10 States by Retail Returns').mark_bar().encode(
            x=alt.X('state', sort=None, title='States'),
            y=alt.Y('retail_returns',
                    title='Retail Returns'),
        )
        st.altair_chart(chart,  use_container_width=True)
