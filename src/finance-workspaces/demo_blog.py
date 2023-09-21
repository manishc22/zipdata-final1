import streamlit.components.v1 as components
import datetime as dt
from datetime import date, time
import datapane as dp
import altair as alt
import pandas as pd
import streamlit as st

from functions.cumulative_sales.trans_tables import *
from functions.cumulative_sales.feeds_post import *
from functions.cumulative_sales.metadata import *
from functions.cumulative_sales.state_db import *
# from functions.feeds_db import *
from functions.cumulative_sales.targets_db import *
from functions.cumulative_sales.alerts_db import *

st.set_page_config(
    page_title="Cumulative Sales",
    layout="centered"
)


tab1, tab2, tab3 = st.tabs(
    ['Dashboard', 'Data Hub', 'Feeds'])

with tab1:

    data = load_monthly_data()
    growth_data = load_growth_data()
    quarterly_data = load_quarterly_data().data

    yearly_data = load_yearly_data().data
    state_ranks = load_state_ranks().data
    q_state_ranks = quarterly_state_ranks().data
    df_ranks = pd.DataFrame.from_records(state_ranks)
    df_q_ranks = pd.DataFrame.from_records(
        q_state_ranks).drop_duplicates(keep='first')
    # print(df_q_ranks)
    df_quarter = pd.DataFrame.from_records(
        quarterly_data)
    df_year = pd.DataFrame.from_records(
        yearly_data[0]['y_value']).sort_values(by=['year'], ascending=False)

    df = pd.DataFrame(data.data).dropna(axis=0).sort_values(
        by=['month_id'], ascending=False)

    df['online_sales'] = round(df['online_sales'] / 1000000, 2)
    df['retail_sales'] = round(df['retail_sales'] / 1000000, 2)
    months = df['month_name'].drop_duplicates()
    df['year'] = df['month_name'].str.slice(4)

    df_growth = pd.DataFrame(growth_data.data)

    col1, col2, col3, col4 = st.columns([2, 0.75, 0.25, 1.25])
    with col1:
        funct = st.radio(label="Select a Term",
                         options=['Monthly', 'Quarterly', 'Yearly'], horizontal=True, key='tab1-term')
    with col4:
        option = st.selectbox('Select a View', options=['Cumulative Metrics',
                                                        'Sales Leaderboards', 'Low Performers', 'State Drilldown'], key='tab1-views')

    st.divider()

    if funct == 'Monthly' and option == 'Cumulative Metrics':
        st.markdown('##### Monthly Cumulative Metrics')
        st.markdown(' ')
        with col2:
            month = st.selectbox(
                'Select Month', options=months, key='mcm')

        col4, col5, col6, col7 = st.columns(4)

        with col4:
            st.metric(label='**:blue[Total Online Sales (*INR million*)]**',
                      value=round((df[df['month_name'] == month]
                                  ['online_sales'].sum()), 2),
                      delta=df_growth[df_growth['month_name'] == month]['online_sales_growth'].values[0])

            # st.metric(label='**:blue[Online Sales Growth (%)]**',
            #           value=df_growth[df_growth['month_name'] == month]['online_sales_growth'])

        with col5:
            st.metric(label='**:blue[Total Retail Sales (*INR million*)]**',
                      value=round(df[df['month_name'] == month]
                                  ['retail_sales'].sum(), 2),
                      delta=df_growth[df_growth['month_name'] == month]['retail_sales_growth'].values[0])
            # st.metric(label='**:blue[Retail Sales Growth (%)]**',
            #           value=df_growth[df_growth['month_name'] == month]['retail_sales_growth'])
        with col6:
            st.metric(label='**:blue[Total Online Orders]**',
                      value='{:,}'.format(
                          df[df['month_name'] == month]['online_orders'].sum()),
                      delta=df_growth[df_growth['month_name'] == month]['online_order_growth'].values[0])
            # st.metric(label='**:blue[Online Order Growth (%)]**',
            #           value=df_growth[df_growth['month_name'] == month]['online_order_growth'])

        with col7:
            st.metric(label='**:blue[Total Retail Orders]**',
                      value='{:,}'.format(
                          df[df['month_name'] == month]['retail_orders'].sum()),
                      delta=df_growth[df_growth['month_name'] == month]['retail_order_growth'].values[0])

            # st.metric(label='**:blue[Retail Order Growth (%)]**',
            #           value=df_growth[df_growth['month_name'] == month]['retail_order_growth'])
        st.divider()

    if funct == 'Monthly' and option == 'Sales Leaderboards':
        with col2:
            month = st.selectbox(
                'Select Month', options=months, key='msl')
        st.markdown('##### Monthly Sales Leaderboards')
        st.markdown(' ')

        col8, col9 = st.columns(2, gap='large')
        with col8:
            df2 = df[df['month_name'] == month].sort_values(
                by='online_sales', ascending=False).head(10)

            chart = alt.Chart(df2, title='Top 10 States by Online Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('online_sales',
                        title='Online Sales (in million)')
            )
            st.altair_chart(chart, use_container_width=True)

        with col9:
            df3 = df[df['month_name'] == month].sort_values(
                by='retail_sales', ascending=False).head(10)

            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df3, title='Top 10 States by Retail Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('retail_sales',
                        title='Retail Sales (in million)'),
            )
            st.altair_chart(chart,  use_container_width=True)

        with col8:
            df4 = df[df['month_name'] == month].sort_values(
                by='growth_online_sales', ascending=False).head(10)
            # print(df)
            # print(df4)
            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df4, title='Top 10 States by MoM Online Sales Growth').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('growth_online_sales',
                        title='Online Sales Growth (%)')
            )
            st.altair_chart(chart, use_container_width=True)

        with col9:
            df5 = df[df['month_name'] == month].sort_values(
                by='growth_retail_sales', ascending=False).head(10)
            # print(df)
            # print(df4)
            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df5, title='Top 10 States by MoM Retail Sales Growth').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('growth_retail_sales',
                        title='Retail Sales Growth (%)')
            )
            st.altair_chart(chart, use_container_width=True)

    if funct == 'Quarterly' and option == 'Cumulative Metrics':
        st.markdown('##### Quarterly Cumulative Metrics')
        st.markdown(' ')
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_quarter['quarter'].drop_duplicates())
#         with col2:
        col4, col5, col6, col7 = st.columns(4)

        with col4:
            st.metric(label='**:blue[Total Online Sales (*INR million*)]**',
                      value=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == 'Cumulative')]['online_sales'].values[0], delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == 'Cumulative')]['growth_online_sales'].values[0])
            # st.metric(label='**:blue[Online Sales Growth (%)]**',
            #           value=round(df_quarter[df_quarter['quarter'] == quarter]['growth_online_sales'].mean(), 2))

        with col5:
            st.metric(label='**:blue[Total Retail Sales (*INR million*)]**',
                      value=df_quarter[(df_quarter['quarter'] == quarter) & (
                          df_quarter['state'] == 'Cumulative')]['retail_sales'].values[0],
                      delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == 'Cumulative')]['growth_retail_sales'].values[0])
            # st.metric(label='**:blue[Retail Sales Growth (%)]**',
            #           value=round(df_quarter[df_quarter['quarter'] == quarter]['growth_retail_sales'].mean(), 2))
        with col6:
            st.metric(label='**:blue[Total Online Orders]**',
                      value=df_quarter[(df_quarter['quarter'] == quarter) & (
                          df_quarter['state'] == 'Cumulative')]['online_orders'].values[0],
                      delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == 'Cumulative')]['growth_online_orders'].values[0])
            # st.metric(label='**:blue[Online Order Growth (%)]**',
            #           value=round(df_quarter[df_quarter['quarter'] == quarter]['growth_online_orders'].mean(), 2))

        with col7:
            st.metric(label='**:blue[Total Retail Orders]**',
                      value=df_quarter[(df_quarter['quarter'] == quarter) & (
                          df_quarter['state'] == 'Cumulative')]['retail_orders'].values[0],
                      delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == 'Cumulative')]['growth_retail_orders'].values[0])

            # st.metric(label='**:blue[Retail Order Growth (%)]**',
            #           value=round(df_quarter[df_quarter['quarter'] == quarter]['growth_retail_orders'].mean(), 2))
        st.divider()

    if funct == 'Quarterly' and option == 'Sales Leaderboards':

        st.markdown('##### Quarterly Sales Leaderboards')
        st.markdown(' ')
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_quarter['quarter'].drop_duplicates())
        col8, col9 = st.columns(2, gap='large')
        with col8:
            df2 = df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] != 'Cumulative')].sort_values(
                by='online_sales', ascending=False).head(10)

            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df2, title='Top 10 States by Online Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('online_sales',
                        title='Online Sales (in million)')
            )
            st.altair_chart(chart, use_container_width=True)

        with col9:
            df3 = df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] != 'Cumulative')].sort_values(
                by='retail_sales', ascending=False).head(10)

            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df3, title='Top 10 States by Retail Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('retail_sales',
                        title='Retail Sales (in million)'),
            )
            st.altair_chart(chart,  use_container_width=True)

        with col8:
            df4 = df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] != 'Cumulative')].sort_values(
                by='growth_online_sales', ascending=False).head(10)
            # print(df)
            # print(df4)
            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df4, title='Top 10 States by QoQ Online Sales Growth').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('growth_online_sales',
                        title='Online Sales Growth (%)')
            )
            st.altair_chart(chart, use_container_width=True)

        with col9:
            df5 = df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] != 'Cumulative')].sort_values(
                by='growth_retail_sales', ascending=False).head(10)
            # print(df)
            # print(df4)
            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df5, title='Top 10 States by QoQ Retail Sales Growth').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('growth_retail_sales',
                        title='Retail Sales Growth (%)')
            )
            st.altair_chart(chart, use_container_width=True)

    if funct == 'Yearly' and option == 'Cumulative Metrics':
        st.markdown('##### Yearly Cumulative Metrics')
        st.markdown(' ')
        with col2:
            year = st.selectbox(
                'Select Year', options=df_year['year'].drop_duplicates())
#          with col2:
        col4, col5, col6, col7 = st.columns(4)
        with col4:
            st.metric(label='**:blue[Total Online Sales (*INR million*)]**',
                      value=round(
                          (df_year[df_year['year'] == year]['total_online_sales'].sum()), 2),
                      delta=round(df_year[df_year['year'] == year]['growth_online_sales'].mean(), 2))
            # st.metric(label='**:blue[Online Sales Growth (%)]**',
            #           value=round(df_year[df_year['year'] == year]['growth_online_sales'].mean(), 2))

        with col5:
            st.metric(label='**:blue[Total Retail Sales (*INR million*)]**',
                      value=round(df_year[df_year['year'] == year]
                                  ['total_retail_sales'].sum(), 2),
                      delta=round(df_year[df_year['year'] == year]['growth_retail_sales'].mean(), 2))
            # st.metric(label='**:blue[Retail Sales Growth (%)]**',
            #           value=round(df_year[df_year['year'] == year]['growth_retail_sales'].mean(), 2))
        with col6:
            st.metric(label='**:blue[Total Online Orders]**',
                      value='{:,}'.format(
                          df_year[df_year['year'] == year]['total_online_orders'].sum()),
                      delta=round(df_year[df_year['year'] == year]['growth_online_orders'].mean(), 2))
            # st.metric(label='**:blue[Online Order Growth (%)]**',
            #           value=round(df_year[df_year['year'] == year]['growth_online_orders'].mean(), 2))

        with col7:
            st.metric(label='**:blue[Total Retail Orders]**',
                      value='{:,}'.format(
                          df_year[df_year['year'] == year]['total_retail_orders'].sum()),
                      delta=round(df_year[df_year['year'] == year]['growth_retail_orders'].mean(), 2))

            # st.metric(label='**:blue[Retail Order Growth (%)]**',
            #           value=round(df_year[df_year['year'] == year]['growth_retail_orders'].mean(), 2))

        st.divider()

    if funct == 'Yearly' and option == 'Sales Leaderboards':
        with col2:
            year = st.selectbox(
                'Select Year', options=df_year['year'].drop_duplicates())
        st.markdown('##### Yearly Sales Leaderboards')
        st.markdown(' ')
        col8, col9 = st.columns(2, gap='large')
        with col8:
            df2 = df_year[df_year['year'] == year].sort_values(
                by='total_online_sales', ascending=False).head(10)

            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df2, title='Top 10 States by Online Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('total_online_sales',
                        title='Online Sales (in million)')
            )
            st.altair_chart(chart, use_container_width=True)

        with col9:
            df3 = df_year[df_year['year'] == year].sort_values(
                by='total_retail_sales', ascending=False).head(10)

            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df3, title='Top 10 States by Retail Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('total_retail_sales',
                        title='Retail Sales (in million)'),
            )
            st.altair_chart(chart,  use_container_width=True)

        with col8:
            df4 = df_year[df_year['year'] == year].sort_values(
                by='growth_online_sales', ascending=False).head(10)
            # print(df)
            # print(df4)
            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df4, title='Top 10 States by YoY Online Sales Growth').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('growth_online_sales',
                        title='Online Sales Growth (%)')
            )
            st.altair_chart(chart, use_container_width=True)

        with col9:
            df5 = df_year[df_year['year'] == year].sort_values(
                by='growth_retail_sales', ascending=False).head(10)

            chart = alt.Chart(df5, title='Top 10 States by YoY Retail Sales Growth').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('growth_retail_sales',
                        title='Retail Sales Growth (%)')
            )
            st.altair_chart(chart, use_container_width=True)

    if funct == 'Monthly' and option == 'State Drilldown':
        with col2:
            month = st.selectbox('Select Month', options=months)
        st.markdown('##### Monthly State Rank & Metrics')
        st.markdown(' ')
        col8, col9, col10 = st.columns([1, 5, 0.5], gap='large')
        with col8:
            sort = st.selectbox(
                'Sort by', options=['Online Sales Rank', 'Retail Sales Rank', 'Online Growth Rank', 'Retail Growth Rank', 'Alphabetically'])
            if sort == 'Online Sales Rank':
                sort = 'online_sales_rank'
            elif sort == 'Retail Sales Rank':
                sort = 'retail_sales_rank'
            elif sort == 'Online Growth Rank':
                sort = 'online_growth_rank'
            elif sort == 'Retail Growth Rank':
                sort = 'retail_growth_rank'
            else:
                sort = 'state'
            df_sort = df_ranks[df_ranks['month_name'] == month].sort_values(
                by=sort)

            st.divider()
            state = st.selectbox(
                'Select State', options=df_sort['state'])
        with col9:

            col3, col4, col5, col6, col7 = st.columns([0.5, 1, 1, 1, 1])

            with col4:
                st.metric(label='**:blue[Online Sales Rank]**',
                          value=df_ranks[(df_ranks['month_name'] == month) & (
                              df_ranks['state'] == state)]['online_sales_rank'],
                          )
                st.divider()
                st.metric(label='**:blue[Total Online Sales (*INR million*)]**',
                          value=df[(df['month_name'] == month) & (
                              df['state'] == state)]['online_sales'],
                          delta=df[(df['month_name'] == month) & (df['state'] == state)]['growth_online_sales'].values[0])

            with col5:
                st.metric(label='**:blue[Retail Sales Rank]**',
                          value=df_ranks[(df_ranks['month_name'] == month) & (
                              df_ranks['state'] == state)]['retail_sales_rank'],
                          )
                st.divider()
                st.metric(label='**:blue[Total Retail Sales (*INR million*)]**',
                          value=df[(df['month_name'] == month) & (
                              df['state'] == state)]['retail_sales'],
                          delta=df[(df['month_name'] == month) & (df['state'] == state)]['growth_retail_sales'].values[0])

            with col6:
                st.metric(label='**:blue[Online Growth Rank]**',
                          value=df_ranks[(df_ranks['month_name'] == month) & (
                              df_ranks['state'] == state)]['online_growth_rank'],
                          )
                st.divider()
                st.metric(label='**:blue[Total Online Orders]**',
                          value=df[(df['month_name'] == month) & (
                              df['state'] == state)]['online_orders'],
                          delta=df[(df['month_name'] == month) & (df['state'] == state)]['growth_online_orders'].values[0])

            with col7:
                st.metric(label='**:blue[Retail Growth Rank]**',
                          value=df_ranks[(df_ranks['month_name'] == month) & (
                              df_ranks['state'] == state)]['retail_growth_rank'],
                          )
                st.divider()
                st.metric(label='**:blue[Total Retail Orders]**',
                          value=df[(df['month_name'] == month) & (
                              df['state'] == state)]['retail_orders'],
                          delta=df[(df['month_name'] == month) & (df['state'] == state)]['growth_retail_orders'].values[0])

    if funct == 'Quarterly' and option == 'State Drilldown':
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_quarter['quarter'].drop_duplicates())
        st.markdown('##### Quarterly State Rank & Metrics')
        st.markdown(' ')
        col8, col9, col10 = st.columns([1, 5, 0.5], gap='large')
        with col8:
            sort = st.selectbox(
                'Sort by', options=['Online Sales Rank', 'Retail Sales Rank', 'Online Growth Rank', 'Retail Growth Rank', 'Alphabetically'])
            if sort == 'Online Sales Rank':
                sort = 'online_sales_rank'
            elif sort == 'Retail Sales Rank':
                sort = 'retail_sales_rank'
            elif sort == 'Online Growth Rank':
                sort = 'online_growth_rank'
            elif sort == 'Retail Growth Rank':
                sort = 'retail_growth_rank'
            else:
                sort = 'state'
            df_sort = df_q_ranks[df_q_ranks['quarter'] == quarter].sort_values(
                by=sort)

            st.divider()
            state = st.selectbox(
                'Select State', options=df_sort['state'])
        with col9:

            col3, col4, col5, col6, col7 = st.columns([0.5, 1, 1, 1, 1])

            with col4:
                st.metric(label='**:blue[Online Sales Rank]**',
                          value=df_q_ranks[(df_q_ranks['quarter'] == quarter) & (
                              df_q_ranks['state'] == state)]['online_sales_rank'],
                          )
                st.divider()

                st.metric(label='**:blue[Total Online Sales (*INR million*)]**',
                          value=df_quarter[(df_quarter['quarter'] == quarter) & (
                              df_quarter['state'] == state)]['online_sales'],
                          delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == state)]['growth_online_sales'].values[0])

            with col5:
                st.metric(label='**:blue[Retail Sales Rank]**',
                          value=df_q_ranks[(df_q_ranks['quarter'] == quarter) & (
                              df_q_ranks['state'] == state)]['retail_sales_rank'],
                          )
                st.divider()
                st.metric(label='**:blue[Total Retail Sales (*INR million*)]**',
                          value=df_quarter[(df_quarter['quarter'] == quarter) & (
                              df_quarter['state'] == state)]['retail_sales'],
                          delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == state)]['growth_retail_sales'].values[0])

            with col6:
                st.metric(label='**:blue[Online Growth Rank]**',
                          value=df_q_ranks[(df_q_ranks['quarter'] == quarter) & (
                              df_q_ranks['state'] == state)]['online_growth_rank'],
                          )
                st.divider()
                st.metric(label='**:blue[Total Online Orders]**',
                          value=df_quarter[(df_quarter['quarter'] == quarter) & (
                              df_quarter['state'] == state)]['online_orders'],
                          delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == state)]['growth_online_orders'].values[0])

            with col7:
                st.metric(label='**:blue[Retail Growth Rank]**',
                          value=df_q_ranks[(df_q_ranks['quarter'] == quarter) & (
                              df_q_ranks['state'] == state)]['retail_growth_rank'],
                          )
                st.divider()
                st.metric(label='**:blue[Total Retail Orders]**',
                          value=df_quarter[(df_quarter['quarter'] == quarter) & (
                              df_quarter['state'] == state)]['retail_orders'],
                          delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == state)]['growth_retail_orders'].values[0])

    if funct == 'Yearly' and option == 'State Drilldown':
        with col2:
            year = st.selectbox(
                'Select Year', options=df_year['year'].drop_duplicates())
        st.markdown('##### Yearly Data')
        st.markdown(' ')

        st.data_editor(df_year[df_year['year'] == year], hide_index=True)

    if funct == 'Monthly' and option == 'Low Performers':
        with col2:
            month = st.selectbox('Select Month', options=months)
        st.markdown('##### Monthly Low Performers')
        st.markdown(' ')
        col8, col9 = st.columns(2, gap='large')
        with col8:
            df2 = df[df['month_name'] == month].sort_values(
                by='online_sales', ascending=False).tail(10)

            chart = alt.Chart(df2, title='Bottom 10 States by Online Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('online_sales',
                        title='Online Sales (in million)')
            )
            st.altair_chart(chart, use_container_width=True)

        with col9:
            df3 = df[(df['month_name'] == month) & (df['retail_sales'] > 0)].sort_values(
                by='retail_sales', ascending=False).tail(10)

            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df3, title='Bottom 10 States by Retail Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('retail_sales',
                        title='Retail Sales (in million)'),
            )
            st.altair_chart(chart,  use_container_width=True)

        with col8:
            df6 = df[(df['month_name'] == month) & (df['online_sales'] > 0) & (df['retail_sales'] == 0)].sort_values(
                by='online_sales', ascending=False).head(10)
            # print(df)
            # print(df4)
            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df6, title='Top 10 States that have Online Sales but no Retail Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('online_sales',
                        title='Online Sales (in million)')
            )
            st.altair_chart(chart, use_container_width=True)

        with col9:
            df['average_growth'] = round(
                (df['growth_retail_sales'] + df['growth_online_sales']) / 2, 2)
            df7 = df[(df['month_name'] == month)].sort_values(
                by='average_growth', ascending=True).head(10)
            # print(df)
            # print(df4)
            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df7, title='States with max decline in overall growth').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('average_growth',
                        title='Average Growth (%)')
            )
            st.altair_chart(chart, use_container_width=True)

    if funct == 'Quarterly' and option == 'Low Performers':
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_quarter['quarter'].drop_duplicates())
        st.markdown('##### Quarterly Low Performers')
        st.markdown(' ')
        col8, col9 = st.columns(2, gap='large')
        with col8:
            df2 = df_quarter[df_quarter['quarter'] == quarter].sort_values(
                by='online_sales', ascending=False).tail(10)

            # print(df2)

            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df2, title='Bottom 10 States by Online Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('online_sales',
                        title='Online Sales (in million)')
            )
            st.altair_chart(chart, use_container_width=True)

        with col9:
            df3 = df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['retail_sales'] > 0)].sort_values(
                by='retail_sales', ascending=False).tail(10)

            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df3, title='Bottom 10 States by Retail Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('retail_sales',
                        title='Retail Sales (in million)'),
            )
            st.altair_chart(chart,  use_container_width=True)

        with col8:
            df6 = df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['online_sales'] > 0) & (df_quarter['retail_sales'] == 0)].sort_values(
                by='online_sales', ascending=False).head(10)
            # print(df)
            # print(df4)
            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df6, title='Top 10 States that have Online Sales but no Retail Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('online_sales',
                        title='Online Sales (in million)')
            )
            st.altair_chart(chart, use_container_width=True)

        with col9:
            df_quarter['average_growth'] = round(
                (df_quarter['growth_retail_sales'] + df_quarter['growth_online_sales']) / 2, 2)
            df7 = df_quarter[(df_quarter['quarter'] == quarter)].sort_values(
                by='average_growth', ascending=True).head(10)
            # print(df)
            # print(df4)
            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df7, title='States with max decline in overall growth').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('average_growth',
                        title='Average Growth (%)')
            )
            st.altair_chart(chart, use_container_width=True)

    if funct == 'Yearly' and option == 'Low Performers':
        with col2:
            year = st.selectbox(
                'Select Year', options=df_year['year'].drop_duplicates())
        st.markdown('##### Yearly Low Performers')
        st.markdown(' ')
        col8, col9 = st.columns(2, gap='large')
        with col8:
            df2 = df_year[df_year['year'] == year].sort_values(
                by='total_online_sales', ascending=False).tail(10)

            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df2, title='Bottom 10 States by Online Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('total_online_sales',
                        title='Online Sales (in million)')
            )
            st.altair_chart(chart, use_container_width=True)

        with col9:
            df3 = df_year[(df_year['year'] == year) & (df_year['total_retail_sales'] > 0)].sort_values(
                by='total_retail_sales', ascending=False).tail(10)

            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df3, title='Bottom 10 States by Retail Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('total_retail_sales',
                        title='Retail Sales (in million)'),
            )
            st.altair_chart(chart,  use_container_width=True)

        with col8:
            df6 = df_year[(df_year['year'] == year) & (df_year['total_online_sales'] > 0) & (df_year['total_retail_sales'] == 0)].sort_values(
                by='total_online_sales', ascending=False).head(10)

            chart = alt.Chart(df6, title='Top 10 States that have Online Sales but no Retail Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('total_online_sales',
                        title='Online Sales (in million)')
            )
            st.altair_chart(chart, use_container_width=True)

        with col9:
            df_year['average_growth'] = round(
                (df_year['growth_retail_sales'] + df_year['growth_online_sales']) / 2, 2)
            df7 = df_year[(df_year['year'] == year)].sort_values(
                by='average_growth', ascending=True).head(10)
            # print(df)
            # print(df4)
            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df7, title='States with max decline in overall growth').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('average_growth',
                        title='Average Growth (%)')
            )
            st.altair_chart(chart, use_container_width=True)
