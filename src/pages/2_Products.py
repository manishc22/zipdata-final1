import streamlit.components.v1 as components
import datetime as dt
from datetime import date, time
import datapane as dp
import altair as alt
import pandas as pd
import streamlit as st
from functions.product_analysis import data
from functions.cumulative_sales.trans_tables import *
from functions.cumulative_sales.feeds_post import *
from functions.cumulative_sales.metadata import *
from functions.cumulative_sales.targets_db import *
from functions.cumulative_sales.alerts_db import *

st.set_page_config(
    page_title="Product Analysis",
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

df_m_p_data = pd.read_csv('./files/product-analysis.csv')
df_q_p_data = pd.read_csv('./files/Product-Analysis-Q.csv')

m_sp_data = data.monthly_state_product_data().data
df_m_sp_data = pd.DataFrame.from_records(
    m_sp_data[0]['value'])
df_m_sp_data['total_sales'] = df_m_sp_data['total_sales']/1000000

q_sp_data = data.quarterly_state_product_data().data
df_q_sp_data = pd.DataFrame.from_records(
    q_sp_data[0]['value'])
df_q_sp_data['total_sales'] = df_q_sp_data['total_sales']/1000000

m_g_data = data.monthly_growth_product_data().data
df_m_g_data = pd.DataFrame.from_records(
    m_g_data[0]['value'])

q_g_data = data.quarterly_growth_product_data().data
df_q_g_data = pd.DataFrame.from_records(
    q_g_data[0]['value'])

tab1, tab2, tab3 = st.tabs(
    ['Dashboard', 'Data Hub', 'Feeds'])

with tab1:
    col1, col2, col3, col4 = st.columns([1.75, 0.75, 1, 1.25], gap='large')
    with col1:
        funct_tab3 = st.radio(label="Select a Term",
                              options=['Monthly', 'Quarterly', 'Yearly'], horizontal=True, key='tab3-term')

    with col4:
        option_tab3 = st.selectbox('Select a View', options=['Cumulative Metrics',
                                                             'Leaderboards', 'State - Drilldowns'], key='tab3-views')
    st.divider()

    if funct_tab3 == 'Monthly' and option_tab3 == 'Cumulative Metrics':
        st.markdown('##### Monthly - Cumulative Metrics')
        st.markdown(' ')
        with col2:
            month = st.selectbox(
                'Select Month', options=df_m_p_data['month_name'].drop_duplicates())

        col8, col9 = st.columns([1, 5], gap='large')

        with col8:

            product_type = st.selectbox(
                'Select a Product Category', options=df_m_p_data['product_type'].drop_duplicates())

        with col9:
            col10, col11, col12 = st.columns(3)
            with col10:
                st.metric(label='**:blue[Total Sales (*INR million*)]**',
                          value=round((df_m_p_data[(df_m_p_data['month_name'] == month) & ((df_m_p_data['product_type'] == product_type))]
                                       ['total_sales'].sum())/1000000, 2))

                st.metric(label='**:blue[Total Sales - Retail (*INR million*)]**',
                          value=round((df_m_p_data[(df_m_p_data['month_name'] == month) & ((df_m_p_data['product_type'] == product_type)) & ((df_m_p_data['channel_type'] == 'retail'))]
                                       ['total_sales'].sum())/1000000, 2))

                st.metric(label='**:blue[Average Discount %]**',
                          value=round((df_m_p_data[(df_m_p_data['month_name'] == month) & ((df_m_p_data['product_type'] == product_type))]
                                       ['discount_pct'].mean()), 2))

            with col11:

                st.metric(label='**:blue[Total Volume Sold]**',
                          value=round((df_m_p_data[(df_m_p_data['month_name'] == month) & ((df_m_p_data['product_type'] == product_type))]
                                       ['total_volume'].sum()), 2))

                st.metric(label='**:blue[Total Sales - Online (*INR million*)]**',
                          value=round((df_m_p_data[(df_m_p_data['month_name'] == month) & ((df_m_p_data['product_type'] == product_type)) & ((df_m_p_data['channel_type'] == 'online'))]
                                       ['total_sales'].sum())/1000000, 2))

            with col12:

                st.metric(label='**:blue[Average Unit Price]**',
                          value=round((df_m_p_data[(df_m_p_data['month_name'] == month) & ((df_m_p_data['product_type'] == product_type))]
                                       ['unit_price'].mean()), 2))

                st.metric(label='**:blue[Average Order Size]**',
                          value=round((df_m_p_data[(df_m_p_data['month_name'] == month) & ((df_m_p_data['product_type'] == product_type))]
                                       ['avg_order_volume'].mean()), 2))

    if funct_tab3 == 'Monthly' and option_tab3 == 'Leaderboards':
        st.markdown('##### Monthly Product - Leaderboards')
        st.markdown(' ')
        with col2:
            month = st.selectbox(
                'Select Month', options=df_m_p_data['month_name'].drop_duplicates())

        col8, col9 = st.columns([1, 5], gap='large')

        with col8:

            product_type = st.selectbox(
                'Select a Product Category', options=df_m_p_data['product_type'].drop_duplicates())

        with col9:
            col10, col11 = st.columns(2, gap='large')

            with col10:
                df3 = df_m_sp_data[(df_m_sp_data['month_name'] == month) & (df_m_sp_data['product_type'] == product_type)].sort_values(
                    by='total_sales', ascending=False).head(10)

                chart = alt.Chart(df3, title=f'Top 10 States by Sales of {product_type}').mark_bar().encode(
                    x=alt.X('state', sort=None, title='States'),
                    y=alt.Y('total_sales',
                            title='Total Sales (in million INR)'),
                )
                st.altair_chart(chart,  use_container_width=True)

            with col11:
                df4 = df_m_sp_data[(df_m_sp_data['month_name'] == month) & (df_m_sp_data['product_type'] == product_type)].sort_values(
                    by='total_volume', ascending=False).head(10)

                chart = alt.Chart(df4, title=f'Top 10 States by Total Volume sold of {product_type}').mark_bar().encode(
                    x=alt.X('state', sort=None, title='States'),
                    y=alt.Y('total_volume',
                            title='Total Volume'),
                )
                st.altair_chart(chart,  use_container_width=True)

            with col10:
                df7 = df_m_p_data[(df_m_p_data['month_name'] == month) & (
                    df_m_p_data['product_type'] == product_type) & (df_m_p_data['channel_type'] == 'online')].groupby(['month_id', 'month_name', 'product_type', 'state']).aggregate({'total_sales': ['sum']}).reset_index()

                df8 = df7.sort_values(
                    by=[('total_sales', 'sum')], ascending=False).head(10)
                df8.columns = df8.columns.get_level_values(
                    0) + '_' + df8.columns.get_level_values(1)
                df8['total_sales_sum'] = df8['total_sales_sum'] / 1000000

                chart = alt.Chart(df8, title=f'Top 10 States by Total Online Sales of {product_type}').mark_bar().encode(
                    x=alt.X('state_', sort=None, title='States'),
                    y=alt.Y('total_sales_sum',
                            title='Total Online Sales (in MM)'),
                )
                st.altair_chart(chart,  use_container_width=True)

            with col10:
                df5 = df_m_sp_data[(df_m_sp_data['month_name'] == month) & (df_m_sp_data['product_type'] == product_type)].sort_values(
                    by='avg_discount_pct', ascending=False).head(10)

                chart = alt.Chart(df5, title=f'Top 10 States by Average Discount % offered for {product_type}').mark_bar().encode(
                    x=alt.X('state', sort=None, title='States'),
                    y=alt.Y('avg_discount_pct',
                            title='Average Discount %'),
                )
                st.altair_chart(chart,  use_container_width=True)

            with col11:
                df9 = df_m_p_data[(df_m_p_data['month_name'] == month) & (
                    df_m_p_data['product_type'] == product_type) & (df_m_p_data['channel_type'] == 'retail')].groupby(['month_id', 'month_name', 'product_type', 'state']).aggregate({'total_sales': ['sum']}).reset_index()

                df10 = df9.sort_values(
                    by=[('total_sales', 'sum')], ascending=False).head(10)
                df10.columns = df10.columns.get_level_values(
                    0) + '_' + df10.columns.get_level_values(1)
                df10['total_sales_sum'] = df10['total_sales_sum'] / 1000000

                chart = alt.Chart(df10, title=f'Top 10 States by Total Retail Sales of {product_type}').mark_bar().encode(
                    x=alt.X('state_', sort=None, title='States'),
                    y=alt.Y('total_sales_sum',
                            title='Total Retail Sales (in MM)'),
                )
                st.altair_chart(chart,  use_container_width=True)

                df6 = df_m_sp_data[(df_m_sp_data['month_name'] == month) & (df_m_sp_data['product_type'] == product_type)].sort_values(
                    by='avg_unit_price', ascending=False).head(10)

                chart = alt.Chart(df6, title=f'Top 10 States by Average Unit Price of {product_type}').mark_bar().encode(
                    x=alt.X('state', sort=None, title='States'),
                    y=alt.Y('avg_unit_price',
                            title='Average Unit Price'),
                )
                st.altair_chart(chart,  use_container_width=True)

    if funct_tab3 == 'Monthly' and option_tab3 == 'State - Drilldowns':
        st.markdown('##### State - Drilldowns')
        st.markdown(' ')
        with col2:
            month = st.selectbox(
                'Select Month', options=df_m_p_data['month_name'].drop_duplicates())

        col8, col9 = st.columns([1, 4], gap='large')

        with col8:

            product_type = st.selectbox(
                'Select a Product Category', options=df_m_p_data['product_type'].drop_duplicates())
            st.divider()

            state = st.selectbox(
                'Select a State', options=df_m_p_data['state'].drop_duplicates())

        with col9:
            col10, col11, col12 = st.columns(3)
            with col10:
                st.metric(label='**:blue[Total Sales (*INR*)]**',
                          value='{:,}'.format(round((df_m_p_data[(df_m_p_data['month_name'] == month) & ((df_m_p_data['product_type'] == product_type)) & ((df_m_p_data['state'] == state))]
                                                     ['total_sales'].sum()), 2)),
                          delta=df_m_g_data[(df_m_g_data['month_name'] == month) & ((df_m_g_data['product_type'] == product_type)) & ((df_m_g_data['state'] == state))]['growth_total_sales'].mean())

                st.metric(label='**:blue[Total Sales - Retail (*INR*)]**',
                          value='{:,}'.format(round((df_m_p_data[(df_m_p_data['month_name'] == month) & ((df_m_p_data['product_type'] == product_type)) & ((df_m_p_data['channel_type'] == 'retail')) & ((df_m_p_data['state'] == state))]
                                                     ['total_sales'].sum()), 2)))

                st.metric(label='**:blue[Total Volume Sold]**',
                          value=round((df_m_p_data[(df_m_p_data['month_name'] == month) & ((df_m_p_data['product_type'] == product_type)) & ((df_m_p_data['state'] == state))]
                                       ['total_volume'].sum()), 2))

            with col11:
                st.metric(label='**:blue[Average Discount %]**',
                          value=round((df_m_p_data[(df_m_p_data['month_name'] == month) & ((df_m_p_data['product_type'] == product_type)) & ((df_m_p_data['state'] == state))]
                                       ['discount_pct'].mean()), 2),
                          delta=df_m_g_data[(df_m_g_data['month_name'] == month) & ((df_m_g_data['product_type'] == product_type)) & ((df_m_g_data['state'] == state))]['growth_avg_discount'].mean())

                st.metric(label='**:blue[Total Sales - Online (*INR*)]**',
                          value='{:,}'.format(round((df_m_p_data[(df_m_p_data['month_name'] == month) & (df_m_p_data['product_type'] == product_type) & (df_m_p_data['channel_type'] == 'online') & (df_m_p_data['state'] == state)]
                                                     ['total_sales'].sum()), 2)))

            with col12:

                st.metric(label='**:blue[Average Unit Price]**',
                          value=round((df_m_p_data[(df_m_p_data['month_name'] == month) & (df_m_p_data['product_type'] == product_type) & (df_m_p_data['state'] == state)]
                                       ['unit_price'].mean()), 2), delta=df_m_g_data[(df_m_g_data['month_name'] == month) & ((df_m_g_data['product_type'] == product_type)) & ((df_m_g_data['state'] == state))]['growth_avg_unit_price'].mean())

                st.metric(label='**:blue[Average Order Size]**',
                          value=round((df_m_p_data[(df_m_p_data['month_name'] == month) & (df_m_p_data['product_type'] == product_type) & (df_m_p_data['state'] == state)]
                                       ['avg_order_volume'].mean()), 2))

    if funct_tab3 == 'Quarterly' and option_tab3 == 'Cumulative Metrics':
        st.markdown('##### Quarterly - Cumulative Metrics')
        st.markdown(' ')
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_q_p_data['quarter'].drop_duplicates())

        col8, col9 = st.columns([1, 5], gap='large')

        with col8:

            product_type = st.selectbox(
                'Select a Product Category', options=df_q_p_data['product_type'].drop_duplicates())

        with col9:
            col10, col11, col12 = st.columns(3)
            with col10:
                st.metric(label='**:blue[Total Sales (*INR million*)]**',
                          value=round((df_q_p_data[(df_q_p_data['quarter'] == quarter) & ((df_q_p_data['product_type'] == product_type))]
                                       ['total_sales'].sum())/1000000, 2))

                st.metric(label='**:blue[Total Sales - Retail (*INR million*)]**',
                          value=round((df_q_p_data[(df_q_p_data['quarter'] == quarter) & ((df_q_p_data['product_type'] == product_type)) & ((df_q_p_data['channel_type'] == 'retail'))]
                                       ['total_sales'].sum())/1000000, 2))

                st.metric(label='**:blue[Average Discount %]**',
                          value=round((df_q_p_data[(df_q_p_data['quarter'] == quarter) & ((df_q_p_data['product_type'] == product_type))]
                                       ['discount_pct'].mean()), 2))

            with col11:

                st.metric(label='**:blue[Total Volume Sold]**',
                          value=round((df_q_p_data[(df_q_p_data['quarter'] == quarter) & ((df_q_p_data['product_type'] == product_type))]
                                       ['total_volume'].sum()), 2))

                st.metric(label='**:blue[Total Sales - Online (*INR million*)]**',
                          value=round((df_q_p_data[(df_q_p_data['quarter'] == quarter) & ((df_q_p_data['product_type'] == product_type)) & ((df_q_p_data['channel_type'] == 'online'))]
                                       ['total_sales'].sum())/1000000, 2))

            with col12:

                st.metric(label='**:blue[Average Unit Price]**',
                          value=round((df_q_p_data[(df_q_p_data['quarter'] == quarter) & ((df_q_p_data['product_type'] == product_type))]
                                       ['unit_price'].mean()), 2))

                st.metric(label='**:blue[Average Order Size]**',
                          value=round((df_q_p_data[(df_q_p_data['quarter'] == quarter) & ((df_q_p_data['product_type'] == product_type))]
                                       ['avg_order_volume'].mean()), 2))

    if funct_tab3 == 'Quarterly' and option_tab3 == 'Leaderboards':
        st.markdown('##### Quarterly Product - Leaderboards')
        st.markdown(' ')
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_q_p_data['quarter'].drop_duplicates())

        col8, col9 = st.columns([1, 5], gap='large')

        with col8:

            product_type = st.selectbox(
                'Select a Product Category', options=df_m_p_data['product_type'].drop_duplicates())

        with col9:
            col10, col11 = st.columns(2, gap='large')

            with col10:
                df3 = df_q_sp_data[(df_q_sp_data['quarter'] == quarter) & (df_q_sp_data['product_type'] == product_type)].sort_values(
                    by='total_sales', ascending=False).head(10)

                chart = alt.Chart(df3, title=f'Top 10 States by Sales of {product_type}').mark_bar().encode(
                    x=alt.X('state', sort=None, title='States'),
                    y=alt.Y('total_sales',
                            title='Total Sales (in million INR)'),
                )
                st.altair_chart(chart,  use_container_width=True)

            with col11:
                df4 = df_q_sp_data[(df_q_sp_data['quarter'] == quarter) & (df_q_sp_data['product_type'] == product_type)].sort_values(
                    by='total_volume', ascending=False).head(10)

                chart = alt.Chart(df4, title=f'Top 10 States by Total Volume sold of {product_type}').mark_bar().encode(
                    x=alt.X('state', sort=None, title='States'),
                    y=alt.Y('total_volume',
                            title='Total Volume'),
                )
                st.altair_chart(chart,  use_container_width=True)

            with col10:
                df7 = df_q_p_data[(df_q_p_data['quarter'] == quarter) & (
                    df_q_p_data['product_type'] == product_type) & (df_q_p_data['channel_type'] == 'online')].groupby(['quarter_id', 'quarter', 'product_type', 'state']).aggregate({'total_sales': ['sum']}).reset_index()

                df8 = df7.sort_values(
                    by=[('total_sales', 'sum')], ascending=False).head(10)
                df8.columns = df8.columns.get_level_values(
                    0) + '_' + df8.columns.get_level_values(1)
                df8['total_sales_sum'] = df8['total_sales_sum'] / 1000000

                chart = alt.Chart(df8, title=f'Top 10 States by Total Online Sales of {product_type}').mark_bar().encode(
                    x=alt.X('state_', sort=None, title='States'),
                    y=alt.Y('total_sales_sum',
                            title='Total Online Sales (in MM)'),
                )
                st.altair_chart(chart,  use_container_width=True)

            with col10:
                df5 = df_q_sp_data[(df_q_sp_data['quarter'] == quarter) & (df_q_sp_data['product_type'] == product_type)].sort_values(
                    by='avg_discount_pct', ascending=False).head(10)

                chart = alt.Chart(df5, title=f'Top 10 States by Average Discount % offered for {product_type}').mark_bar().encode(
                    x=alt.X('state', sort=None, title='States'),
                    y=alt.Y('avg_discount_pct',
                            title='Average Discount %'),
                )
                st.altair_chart(chart,  use_container_width=True)

            with col11:
                df9 = df_q_p_data[(df_q_p_data['quarter'] == quarter) & (
                    df_q_p_data['product_type'] == product_type) & (df_q_p_data['channel_type'] == 'retail')].groupby(['quarter_id', 'quarter', 'product_type', 'state']).aggregate({'total_sales': ['sum']}).reset_index()

                df10 = df9.sort_values(
                    by=[('total_sales', 'sum')], ascending=False).head(10)
                df10.columns = df10.columns.get_level_values(
                    0) + '_' + df10.columns.get_level_values(1)
                df10['total_sales_sum'] = df10['total_sales_sum'] / 1000000

                chart = alt.Chart(df10, title=f'Top 10 States by Total Retail Sales of {product_type}').mark_bar().encode(
                    x=alt.X('state_', sort=None, title='States'),
                    y=alt.Y('total_sales_sum',
                            title='Total Retail Sales (in MM)'),
                )
                st.altair_chart(chart,  use_container_width=True)

                df6 = df_q_sp_data[(df_q_sp_data['quarter'] == quarter) & (df_q_sp_data['product_type'] == product_type)].sort_values(
                    by='avg_unit_price', ascending=False).head(10)

                chart = alt.Chart(df6, title=f'Top 10 States by Average Unit Price of {product_type}').mark_bar().encode(
                    x=alt.X('state', sort=None, title='States'),
                    y=alt.Y('avg_unit_price',
                            title='Average Unit Price'),
                )
                st.altair_chart(chart,  use_container_width=True)

    if funct_tab3 == 'Quarterly' and option_tab3 == 'State - Drilldowns':
        st.markdown('##### (Quarterly) State - Drilldowns')
        st.markdown(' ')
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_q_p_data['quarter'].drop_duplicates())

        col8, col9 = st.columns([1, 5], gap='large')

        with col8:

            product_type = st.selectbox(
                'Select a Product Category', options=df_q_p_data['product_type'].drop_duplicates())
            st.divider()

            state = st.selectbox(
                'Select a State', options=df_q_p_data['state'].drop_duplicates())

        with col9:
            col10, col11, col12 = st.columns(3)
            with col10:
                st.metric(label='**:blue[Total Sales (*INR*)]**',
                          value='{:,}'.format(round((df_q_p_data[(df_q_p_data['quarter'] == quarter) & ((df_q_p_data['product_type'] == product_type)) & ((df_q_p_data['state'] == state))]
                                                     ['total_sales'].sum()), 2)),
                          delta=df_q_g_data[(df_q_g_data['quarter'] == quarter) & ((df_q_g_data['product_type'] == product_type)) & ((df_q_g_data['state'] == state))]['growth_total_sales'].mean())

                st.metric(label='**:blue[Total Sales - Retail (*INR*)]**',
                          value='{:,}'.format(round((df_q_p_data[(df_q_p_data['quarter'] == quarter) & ((df_q_p_data['product_type'] == product_type)) & ((df_q_p_data['channel_type'] == 'retail')) & ((df_q_p_data['state'] == state))]
                                                     ['total_sales'].sum()), 2)))

                st.metric(label='**:blue[Total Volume Sold]**',
                          value=round((df_q_p_data[(df_q_p_data['quarter'] == quarter) & ((df_q_p_data['product_type'] == product_type)) & ((df_q_p_data['state'] == state))]
                                       ['total_volume'].sum()), 2))

            with col11:
                st.metric(label='**:blue[Average Discount %]**',
                          value=round((df_q_p_data[(df_q_p_data['quarter'] == quarter) & ((df_q_p_data['product_type'] == product_type)) & ((df_q_p_data['state'] == state))]
                                       ['discount_pct'].mean()), 2),
                          delta=df_q_g_data[(df_q_g_data['quarter'] == quarter) & ((df_q_g_data['product_type'] == product_type)) & ((df_q_g_data['state'] == state))]['growth_avg_discount'].mean())

                st.metric(label='**:blue[Total Sales - Online (*INR*)]**',
                          value='{:,}'.format(round((df_q_p_data[(df_q_p_data['quarter'] == quarter) & (df_q_p_data['product_type'] == product_type) & (df_q_p_data['channel_type'] == 'online') & (df_q_p_data['state'] == state)]
                                                     ['total_sales'].sum()), 2)))

            with col12:

                st.metric(label='**:blue[Average Unit Price]**',
                          value=round((df_q_p_data[(df_q_p_data['quarter'] == quarter) & (df_q_p_data['product_type'] == product_type) & (df_q_p_data['state'] == state)]
                                       ['unit_price'].mean()), 2), delta=df_q_g_data[(df_q_g_data['quarter'] == quarter) & ((df_q_g_data['product_type'] == product_type)) & ((df_q_g_data['state'] == state))]['growth_avg_unit_price'].mean())

                st.metric(label='**:blue[Average Order Size]**',
                          value=round((df_q_p_data[(df_q_p_data['quarter'] == quarter) & (df_q_p_data['product_type'] == product_type) & (df_q_p_data['state'] == state)]
                                       ['avg_order_volume'].mean()), 2))

with tab2:

    workspace = 'Product Analysis'
    col1, col2, col3, col4, col5 = st.columns([1, 1, 0.5, 2, 1])

    with col1:
        option = st.selectbox('*Select Data Type*', options=[
            'Transactional', 'Analysis', 'Insights'])
    trans_metadata = trans_metadata(workspace)
    views_metadata = views_metadata(workspace)
    options_trans = trans_metadata['table_name']
    options_views = views_metadata['table_name']
    # print(options_trans.shape[0])
    if options_trans.shape[0] != 0 and option == 'Transactional':
        with col2:
            table_name = st.selectbox(
                '*Table*', options=options_trans)
            # with st.spinner('Loading'):
            df_table_data_raw = pd.DataFrame(
                trans_data(table_name).data)
            df_table_data = hide_columns(df_table_data_raw)
        with col3:
            if 'month_name' in df_table_data.columns:
                df_months = get_months(df_table_data_raw)

                term = st.selectbox(
                    '*Term*', options=df_months['month_name'].values)
                if df_table_data.shape[0] > 0:
                    with st.spinner('Loading'):
                        v = dp.DataTable(
                            df_table_data[df_table_data['month_name'] == term])

            else:
                if df_table_data.shape[0] > 0:
                    with st.spinner('Loading'):
                        v = dp.DataTable(df_table_data)

    elif option == 'Analysis' and options_views.shape[0] != 0:
        with col2:
            table_name = st.selectbox(
                '*Tables*', options=views_metadata['table_name'])
            with st.spinner('Loading'):
                df_table_data = pd.DataFrame(
                    trans_data(table_name).data)

        with col3:
            if 'month_name' in df_table_data.columns:
                df_months = df_table_data['month_name'].drop_duplicates()
                term = st.selectbox(
                    '*Term*', options=df_months)
                if df_table_data.shape[0] > 0:
                    with st.spinner('Loading'):
                        v = dp.DataTable(
                            df_table_data[df_table_data['month_name'] == term])

            elif 'quarter' in df_table_data.columns:
                df_quarters = df_table_data['quarter'].drop_duplicates()
                term = st.selectbox(
                    '*Term*', options=df_quarters)
                if df_table_data.shape[0] > 0:
                    with st.spinner('Loading'):
                        v = dp.DataTable(
                            df_table_data[df_table_data['quarter'] == term])

            else:
                if df_table_data.shape[0] > 0:
                    with st.spinner('Loading'):
                        v = dp.DataTable(df_table_data)
    else:
        df_table_data = pd.DataFrame()
        # description = table_label
    st.divider()
    with col5:
        view = st.selectbox(
            '*Select a View*', options=['Interact with Data', 'Set Targets', 'Set Alerts'])

    if view == 'Interact with Data':
        st.markdown('##### Interactive Datatables - Sort, Filter and Query')
        if df_table_data.shape[0] > 0:
            with st.spinner('Loading'):
                html = dp.stringify_report(v)
                components.html(html, height=600, width=None, scrolling=False)
        else:
            st.write('#### No data in this table')

    if view == 'Set Targets':
        st.markdown(
            '##### Set Targets for any Metric and Dimension, for any future Term')
        df_targets = pd.DataFrame()
        dataframe, df_targets1 = get_targets(df_targets, workspace)
        df_targets = dataframe
        # df_targets = pd.DataFrame(columns=['ID',
        #                                    'Workspace', 'Target Name', 'Target Rule', 'Term', 'Update Frequency', 'Delivery Time', 'Status'])

        if term[0] == 'Q':
            quarter_term = get_quarters(term)
            term = quarter_term['label'].values
        else:
            month_term = target_months(term)
            term = month_term['month_name'].values
        col1, col2, col3 = st.columns([0.5, 4, 0.5], gap='large')
        with col2:
            with st.form('Targets'):
                df_edits = st.data_editor(
                    df_targets, key='target_editor', hide_index=True, use_container_width=True, num_rows='dynamic', disabled=False,
                    column_config={'ID': None,
                                   'Workspace': None,
                                   'Target Name': st.column_config.Column(
                                       width="medium",
                                       required=True),
                                   'Target Rule': st.column_config.Column(
                                       width="large",
                                       required=True),
                                   'Term': st.column_config.SelectboxColumn(
                                       "Term", options=term),
                                   "Update Frequency": st.column_config.SelectboxColumn(
                                       "Update Frequency", options=['Daily', 'Weekly', 'Monthly', 'Quarter'], width='small', required=True),
                                   "Delivery Time": st.column_config.TimeColumn(
                                       "Delivery Time",
                                       format="hh:mm a",
                                       step=60, required=True, width='small'),
                                   "Status": st.column_config.SelectboxColumn(
                                       "Status", options=['Active', 'Complete', 'Inactive'], width='small', required=True),
                                   })

                df_insert = pd.DataFrame.from_dict(
                    st.session_state['target_editor']['added_rows'])

                df_update = pd.DataFrame.from_records(
                    st.session_state['target_editor']['edited_rows'])

                df_delete = pd.DataFrame.from_dict(
                    st.session_state['target_editor']['deleted_rows'])

                submit = st.form_submit_button(
                    'Submit')
            if submit == True and df_insert.shape[0] > 0:
                with st.spinner('Please wait'):
                    df_insert['Workspace'] = workspace
                    data_insert = targets_insert(df_insert)
                    if data_insert:
                        st.success('Successfully Inserted')

            if submit == True and df_update.shape[0] > 0:
                df_update = update_preprocess_targets(df_update, df_targets1)

                with st.spinner('Please wait'):
                    update = update_targets(df_update)
                    if update:
                        st.success('Successfully Updated')

    if view == 'Set Alerts':
        st.markdown('##### Set Rule based Triggers')
        df_alerts = pd.DataFrame()
        dataframe, df_alerts1 = get_alerts(df_alerts, workspace)
        df_alerts = dataframe
        # df_alerts = pd.DataFrame(columns=['ID',
        #                                    'Workspace', 'Target Name', 'Target Rule', 'Term', 'Update Frequency', 'Delivery Time', 'Status'])

        if term[0] == 'Q':
            quarter_term = get_quarters(term)
            term = quarter_term['label'].values
        else:
            month_term = target_months(term)
            term = month_term['month_name'].values
        col1, col2, col3 = st.columns([0.5, 4, 0.5], gap='large')
        with col2:
            with st.form('Alerts'):
                df_edits = st.data_editor(
                    df_alerts, key='alert_editor1', hide_index=True, use_container_width=True, num_rows='dynamic', disabled=False,
                    column_config={'ID': None,
                                   'Workspace': None,
                                   'Target Name': st.column_config.Column(
                                       width="medium",
                                       required=True),
                                   'Target Rule': st.column_config.Column(
                                       width="large",
                                       required=True),
                                   "Status": st.column_config.SelectboxColumn(
                                       "Status", options=['Active', 'Complete', 'Inactive'], width='small', required=True),
                                   })

                df_insert = pd.DataFrame.from_dict(
                    st.session_state['alert_editor1']['added_rows'])

                df_update = pd.DataFrame.from_records(
                    st.session_state['alert_editor1']['edited_rows'])

                df_delete = pd.DataFrame.from_dict(
                    st.session_state['alert_editor1']['deleted_rows'])

                submit = st.form_submit_button(
                    'Submit')
            if submit == True and df_insert.shape[0] > 0:
                with st.spinner('Please wait'):
                    df_insert['Workspace'] = workspace

                    data_insert = alerts_insert(df_insert)
                    if data_insert:
                        st.success('Successfully Inserted')

            if submit == True and df_update.shape[0] > 0:
                df_update = update_preprocess_alerts(df_update, df_alerts1)

                with st.spinner('Please wait'):
                    update = update_alerts(df_update)
                    if update:
                        st.success('Successfully Updated')

with tab3:
    now = dt.date.today()

    min_date = dt.datetime.strptime('01-01-2020', '%m-%d-%Y').date()
    date_value = now.replace(day=1)
    col1, col2, col3, col4, col5 = st.columns([1, 1.5, 4, 1, 1])

    with col1:
        feed_type = st.selectbox(
            '*Feed Type*', options=['All', 'Posts', 'Alert', 'Target'])

    with col4:
        start_dt = st.date_input(
            "*Enter Start Date*", min_value=min_date, max_value=now, value=date_value)
    with col5:
        end_dt = st.date_input(
            "*Enter End Date*", min_value=start_dt, max_value=now)
    st.divider()

    st.markdown(
        '##### Updates about Alerts, Targets, and all other Analysis')
    st.markdown(' ')
    if feed_type == 'All':
        feed_type = ''

    col1, col2, col3 = st.columns([0.5, 4, 0.5], gap='large')
    posts = load_feed_posts(workspace)
    df_posts = pd.DataFrame.from_records(posts)
    i = 0
    while i < df_posts.shape[0]:
        link = df_posts.loc[i, 'link']
        published_at = df_posts.loc[i, 'created_at']
        term = df_posts.loc[i, 'term']
        title = df_posts.loc[i, 'feed_name']
        date, time = published_at.split('T')
        time1, time2 = time.split('.')
        label = f'**{title}**' + '  |   ' + date + ',' + '  ' + time1

        with col2:
            with st.expander(label=label):
                components.iframe(link, height=600,
                                  width=None, scrolling=False)
        i = i + 1
