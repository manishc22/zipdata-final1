import streamlit.components.v1 as components
import datetime as dt
from datetime import date, time
import datapane as dp
import altair as alt
import pandas as pd
import streamlit as st
import numpy as np

from functions.cumulative_sales.trans_tables import *
from functions.cumulative_sales.feeds_post import *
from functions.cumulative_sales.metadata import *
from functions.cumulative_sales.state_db import *
# from functions.feeds_db import *
from functions.cumulative_sales.targets_db import *
from functions.cumulative_sales.alerts_db import *
from functions.feeds.demo import *
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

    col1, col2, col4 = st.columns([1, 1, 1.5])
    with col1:
        funct = st.selectbox('Select a Term',
                             options=['Monthly', 'Quarterly', 'Yearly'], key='tab1-term')
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

        col4, col5 = st.columns(2)

        with col4:
            st.metric(label='**:blue[Total Online Sales (*INR million*)]**',
                      value=round((df[df['month_name'] == month]
                                  ['online_sales'].sum()), 2),
                      delta=df_growth[df_growth['month_name'] == month]['online_sales_growth'].values[0])

            st.metric(label='**:blue[Total Online Orders]**',
                      value='{:,}'.format(
                          df[df['month_name'] == month]['online_orders'].sum()),
                      delta=df_growth[df_growth['month_name'] == month]['online_order_growth'].values[0])

        with col5:
            st.metric(label='**:blue[Total Retail Sales (*INR million*)]**',
                      value=round(df[df['month_name'] == month]
                                  ['retail_sales'].sum(), 2),
                      delta=df_growth[df_growth['month_name'] == month]['retail_sales_growth'].values[0])
            st.metric(label='**:blue[Total Retail Orders]**',
                      value='{:,}'.format(
                          df[df['month_name'] == month]['retail_orders'].sum()),
                      delta=df_growth[df_growth['month_name'] == month]['retail_order_growth'].values[0])

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
        col4, col5 = st.columns(2)

        with col4:
            st.metric(label='**:blue[Total Online Sales (*INR million*)]**',
                      value=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == 'Cumulative')]['online_sales'].values[0], delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == 'Cumulative')]['growth_online_sales'].values[0])
            # st.metric(label='**:blue[Online Sales Growth (%)]**',
            #           value=round(df_quarter[df_quarter['quarter'] == quarter]['growth_online_sales'].mean(), 2))
            st.metric(label='**:blue[Total Online Orders]**',
                      value=df_quarter[(df_quarter['quarter'] == quarter) & (
                          df_quarter['state'] == 'Cumulative')]['online_orders'].values[0],
                      delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == 'Cumulative')]['growth_online_orders'].values[0])
        with col5:
            st.metric(label='**:blue[Total Retail Sales (*INR million*)]**',
                      value=df_quarter[(df_quarter['quarter'] == quarter) & (
                          df_quarter['state'] == 'Cumulative')]['retail_sales'].values[0],
                      delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == 'Cumulative')]['growth_retail_sales'].values[0])

            st.metric(label='**:blue[Total Retail Orders]**',
                      value=df_quarter[(df_quarter['quarter'] == quarter) & (
                          df_quarter['state'] == 'Cumulative')]['retail_orders'].values[0],
                      delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == 'Cumulative')]['growth_retail_orders'].values[0])
            # st.metric(label='**:blue[Retail Sales Growth (%)]**',
            #           value=round(df_quarter[df_quarter['quarter'] == quarter]['growth_retail_sales'].mean(), 2))

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
        col8, col9 = st.columns([1, 2], gap='large')
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

            col4, col5 = st.columns([1, 1])

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
                st.metric(label='**:blue[Online Growth Rank]**',
                          value=df_ranks[(df_ranks['month_name'] == month) & (
                              df_ranks['state'] == state)]['online_growth_rank'],
                          )
                st.metric(label='**:blue[Total Online Orders]**',
                          value=df[(df['month_name'] == month) & (
                              df['state'] == state)]['online_orders'],
                          delta=df[(df['month_name'] == month) & (df['state'] == state)]['growth_online_orders'].values[0])

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
                st.metric(label='**:blue[Retail Growth Rank]**',
                          value=df_ranks[(df_ranks['month_name'] == month) & (
                              df_ranks['state'] == state)]['retail_growth_rank'],
                          )
                st.metric(label='**:blue[Total Retail Orders]**',
                          value=df[(df['month_name'] == month) & (
                              df['state'] == state)]['retail_orders'],
                          delta=df[(df['month_name'] == month) & (df['state'] == state)]['growth_retail_orders'].values[0])

            # with col6:
            #     st.metric(label='**:blue[Online Growth Rank]**',
            #               value=df_ranks[(df_ranks['month_name'] == month) & (
            #                   df_ranks['state'] == state)]['online_growth_rank'],
            #               )
            #     st.divider()
            #     st.metric(label='**:blue[Total Online Orders]**',
            #               value=df[(df['month_name'] == month) & (
            #                   df['state'] == state)]['online_orders'],
            #               delta=df[(df['month_name'] == month) & (df['state'] == state)]['growth_online_orders'].values[0])

            # with col7:
            #     st.metric(label='**:blue[Retail Growth Rank]**',
            #               value=df_ranks[(df_ranks['month_name'] == month) & (
            #                   df_ranks['state'] == state)]['retail_growth_rank'],
            #               )
            #     st.divider()
            #     st.metric(label='**:blue[Total Retail Orders]**',
            #               value=df[(df['month_name'] == month) & (
            #                   df['state'] == state)]['retail_orders'],
            #               delta=df[(df['month_name'] == month) & (df['state'] == state)]['growth_retail_orders'].values[0])

    if funct == 'Quarterly' and option == 'State Drilldown':
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_quarter['quarter'].drop_duplicates())
        st.markdown('##### Quarterly State Rank & Metrics')
        st.markdown(' ')
        col8, col9 = st.columns([1, 2], gap='large')
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

            col4, col5 = st.columns([1, 1])

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

                st.metric(label='**:blue[Online Growth Rank]**',
                          value=df_q_ranks[(df_q_ranks['quarter'] == quarter) & (
                              df_q_ranks['state'] == state)]['online_growth_rank'],
                          )
                # st.divider()
                st.metric(label='**:blue[Total Online Orders]**',
                          value=df_quarter[(df_quarter['quarter'] == quarter) & (
                              df_quarter['state'] == state)]['online_orders'],
                          delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == state)]['growth_online_orders'].values[0])

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

                st.metric(label='**:blue[Retail Growth Rank]**',
                          value=df_q_ranks[(df_q_ranks['quarter'] == quarter) & (
                              df_q_ranks['state'] == state)]['retail_growth_rank'],
                          )

                st.metric(label='**:blue[Total Retail Orders]**',
                          value=df_quarter[(df_quarter['quarter'] == quarter) & (
                              df_quarter['state'] == state)]['retail_orders'],
                          delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == state)]['growth_retail_orders'].values[0])

            # with col6:
            #     st.metric(label='**:blue[Online Growth Rank]**',
            #               value=df_q_ranks[(df_q_ranks['quarter'] == quarter) & (
            #                   df_q_ranks['state'] == state)]['online_growth_rank'],
            #               )
            #     st.divider()
            #     st.metric(label='**:blue[Total Online Orders]**',
            #               value=df_quarter[(df_quarter['quarter'] == quarter) & (
            #                   df_quarter['state'] == state)]['online_orders'],
            #               delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == state)]['growth_online_orders'].values[0])

            # with col7:
            #     st.metric(label='**:blue[Retail Growth Rank]**',
            #               value=df_q_ranks[(df_q_ranks['quarter'] == quarter) & (
            #                   df_q_ranks['state'] == state)]['retail_growth_rank'],
            #               )
            #     st.divider()
            #     st.metric(label='**:blue[Total Retail Orders]**',
            #               value=df_quarter[(df_quarter['quarter'] == quarter) & (
            #                   df_quarter['state'] == state)]['retail_orders'],
            #               delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == state)]['growth_retail_orders'].values[0])

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

with tab2:
    dp.login(token="8a6aa6da0365af22aa8b58e103a9532e12af9dc3")
    workspace = 'Cumulative Sales'
    col1, col2, col3, col5 = st.columns([1, 1, 0.75, 1])

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
            df_dtype = pd.Series(df_table_data.dtypes)

            print(df_dtype.shape)
            i = 0
            while i < df_dtype.shape[0]:
                if df_dtype.values[i] == 'int64':
                    df_table_data = df_table_data.astype(
                        {df_dtype.index[i]: np.int32})
                i = i + 1
            print(df_table_data.dtypes)
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
        # col1, col2, col3 = st.columns([0.5, 4, 0.5], gap='large')

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
        # col1, col2, col3 = st.columns([0.5, 4, 0.5], gap='large')
        # with col2:
        with st.form('Alerts'):
            df_edits = st.data_editor(
                df_alerts, key='alert_editor', hide_index=True, use_container_width=True, num_rows='dynamic', disabled=False,
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
                st.session_state['alert_editor']['added_rows'])

            df_update = pd.DataFrame.from_records(
                st.session_state['alert_editor']['edited_rows'])

            df_delete = pd.DataFrame.from_dict(
                st.session_state['alert_editor']['deleted_rows'])

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
    col1, col2, col4, col5 = st.columns([1, 0.5, 1, 1])

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

    # col1, col2, col3 = st.columns([0.5, 4, 0.5], gap='large')
    posts = load_feed_posts(workspace)
    df_posts = pd.DataFrame.from_records(posts)
    i = 0
    while i < df_posts.shape[0]:
        # link = df_posts.loc[i, 'link']
        link = feed_gen()
        published_at = df_posts.loc[i, 'created_at']
        term = df_posts.loc[i, 'term']
        title = df_posts.loc[i, 'feed_name']
        date, time = published_at.split('T')
        time1, time2 = time.split('.')
        label = f'**{title}**' + '  |   ' + date + ',' + '  ' + time1

        with st.expander(label=label):
            components.html(link, height=600,
                            width=None, scrolling=False)
            # components.iframe(link, height=600,
            #                   width=None, scrolling=False)
        i = i + 1
