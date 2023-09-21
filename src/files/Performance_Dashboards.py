import streamlit as st
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Zipdata - Advanced Analytics Platform",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",

)


load_dotenv()


@st.cache_resource
def load_supabase():
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase


supabase = load_supabase()


# df1 = df[['month_name', 'state', 'online_sales']]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ['Cumulative Sales', 'Retail Operations', 'Product Analysis ', 'Customer Location Analysis', 'Returns', 'Expenses'])


with tab1:

    @st.cache_data
    def load_monthly_data():
        data = supabase.table('monthly_state_performance').select(
            "*").execute()
        return data

    @st.cache_data
    def load_growth_data():
        growth_data = supabase.table('monthly_sales_growth').select(
            "*").execute()
        return growth_data

    @st.cache_data
    def load_quarterly_data():
        quarterly_data = supabase.table('s_states_tbl').select(
            "q_value").eq('name', 'Cumulative').execute()
        return quarterly_data

    @st.cache_data
    def load_yearly_data():
        yearly_data = supabase.table('s_states_tbl').select(
            "y_value").eq('name', 'Cumulative').execute()
        return yearly_data

    data = load_monthly_data()
    growth_data = load_growth_data()
    quarterly_data = load_quarterly_data().data
    yearly_data = load_yearly_data().data

    df_quarter = pd.DataFrame.from_records(quarterly_data[0]['q_value'])
    df_year = pd.DataFrame.from_records(yearly_data[0]['y_value'])
    print(df_year)
    df = pd.DataFrame(data.data).dropna(axis=0)
    df['online_sales'] = df['online_sales'] / 1000000
    df['retail_sales'] = df['retail_sales'] / 1000000

    df['year'] = df['month_name'].str.slice(4)

    df_growth = pd.DataFrame(growth_data.data)

    st.markdown('    ')
    # value='{:,}'.format(df[df['month_name'] == month]['online_sales'].sum()/1000000))
    col1, col2, col3, col4 = st.columns([2, 0.75, 3, 1], gap='large')
    # with col1:
    with col1:
        funct = st.radio(label="Select a Term",
                         options=['Monthly', 'Quarterly', 'Yearly'], horizontal=True)
    with col3:
        st.container()
    option = st.sidebar.selectbox('Select a View', options=['Metrics',
                                                            'Sales Leaderboards', 'Risk Analysis', 'Datatables'])
    # with col4:
    # st.markdown('### |')
    st.divider()
    if funct == 'Monthly':
        with col2:
            month = st.selectbox('Select Month', options=df['month_name'])
#          with col2:
        col4, col5, col6, col7 = st.columns(4)
        with col4:
            st.metric(label='**:blue[Total Online Sales (*INR million*)]**',
                      value=round((df[df['month_name'] == month]['online_sales'].sum()), 2))
            st.metric(label='**:blue[Online Sales Growth (%)]**',
                      value=df_growth[df_growth['month_name'] == month]['online_sales_growth'])

        with col5:
            st.metric(label='**:blue[Total Retail Sales (*INR million*)]**',
                      value=round(df[df['month_name'] == month]['retail_sales'].sum(), 2))
            st.metric(label='**:blue[Retail Sales Growth (%)]**',
                      value=df_growth[df_growth['month_name'] == month]['retail_sales_growth'])
        with col6:
            st.metric(label='**:blue[Total Online Orders]**',
                      value='{:,}'.format(df[df['month_name'] == month]['online_orders'].sum()))
            st.metric(label='**:blue[Online Order Growth (%)]**',
                      value=df_growth[df_growth['month_name'] == month]['online_order_growth'])

        with col7:
            st.metric(label='**:blue[Total Retail Orders]**',
                      value='{:,}'.format(df[df['month_name'] == month]['retail_orders'].sum()))

            st.metric(label='**:blue[Retail Order Growth (%)]**',
                      value=df_growth[df_growth['month_name'] == month]['retail_order_growth'])
        st.divider()

        st.markdown('##### Monthly Sales Leaderboards')
        st.markdown(' ')

        col8, col9 = st.columns(2, gap='large')
        with col8:
            df2 = df[df['month_name'] == month].sort_values(
                by='online_sales', ascending=False).head(10)

            # print(df2)

            # st.bar_chart(df2, x='state', y='online_sales')
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

    elif funct == 'Quarterly':
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_quarter['quarter'].drop_duplicates())
#         with col2:
        col4, col5, col6, col7 = st.columns(4)
        with col4:
            st.metric(label='**:blue[Total Online Sales (*INR million*)]**',
                      value=round((df_quarter[df_quarter['quarter'] == quarter]['total_online_sales'].sum()), 2))
            st.metric(label='**:blue[Online Sales Growth (%)]**',
                      value=round(df_quarter[df_quarter['quarter'] == quarter]['growth_online_sales'].mean(), 2))

        with col5:
            st.metric(label='**:blue[Total Retail Sales (*INR million*)]**',
                      value=round(df_quarter[df_quarter['quarter'] == quarter]['total_retail_sales'].sum(), 2))
            st.metric(label='**:blue[Retail Sales Growth (%)]**',
                      value=round(df_quarter[df_quarter['quarter'] == quarter]['growth_retail_sales'].mean(), 2))
        with col6:
            st.metric(label='**:blue[Total Online Orders]**',
                      value='{:,}'.format(df_quarter[df_quarter['quarter'] == quarter]['total_online_orders'].sum()))
            st.metric(label='**:blue[Online Order Growth (%)]**',
                      value=round(df_quarter[df_quarter['quarter'] == quarter]['growth_online_orders'].mean(), 2))

        with col7:
            st.metric(label='**:blue[Total Retail Orders]**',
                      value='{:,}'.format(df_quarter[df_quarter['quarter'] == quarter]['total_retail_orders'].sum()))

            st.metric(label='**:blue[Retail Order Growth (%)]**',
                      value=round(df_quarter[df_quarter['quarter'] == quarter]['growth_retail_orders'].mean(), 2))
        st.divider()

        st.markdown('##### Quarterly Sales Leaderboards')
        st.markdown(' ')
        col8, col9 = st.columns(2, gap='large')
        with col8:
            df2 = df_quarter[df_quarter['quarter'] == quarter].sort_values(
                by='total_online_sales', ascending=False).head(10)

            # print(df2)

            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df2, title='Top 10 States by Online Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('total_online_sales',
                        title='Online Sales (in million)')
            )
            st.altair_chart(chart, use_container_width=True)

        with col9:
            df3 = df_quarter[df_quarter['quarter'] == quarter].sort_values(
                by='total_retail_sales', ascending=False).head(10)

            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df3, title='Top 10 States by Retail Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('total_retail_sales',
                        title='Retail Sales (in million)'),
            )
            st.altair_chart(chart,  use_container_width=True)

        with col8:
            df4 = df_quarter[df_quarter['quarter'] == quarter].sort_values(
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
            df5 = df_quarter[df_quarter['quarter'] == quarter].sort_values(
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

        with col8:
            df6 = df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['total_online_sales'] > 0) & (df_quarter['total_retail_sales'] == 0)].sort_values(
                by='total_online_sales', ascending=False).head(10)
            # print(df)
            # print(df4)
            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df6, title='Top 10 States that have Online Sales but no Retail Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('total_online_sales',
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
    else:
        if funct == 'Yearly':
            with col2:
                year = st.selectbox(
                    'Select Year', options=df_year['year'].drop_duplicates())
    #          with col2:
            col4, col5, col6, col7 = st.columns(4)
            with col4:
                st.metric(label='**:blue[Total Online Sales (*INR million*)]**',
                          value=round((df_year[df_year['year'] == year]['total_online_sales'].sum()), 2))
                st.metric(label='**:blue[Online Sales Growth (%)]**',
                          value=round(df_year[df_year['year'] == year]['growth_online_sales'].mean(), 2))

            with col5:
                st.metric(label='**:blue[Total Retail Sales (*INR million*)]**',
                          value=round(df_year[df_year['year'] == year]['total_retail_sales'].sum(), 2))
                st.metric(label='**:blue[Retail Sales Growth (%)]**',
                          value=round(df_year[df_year['year'] == year]['growth_retail_sales'].mean(), 2))
            with col6:
                st.metric(label='**:blue[Total Online Orders]**',
                          value='{:,}'.format(df_year[df_year['year'] == year]['total_online_orders'].sum()))
                st.metric(label='**:blue[Online Order Growth (%)]**',
                          value=round(df_year[df_year['year'] == year]['growth_online_orders'].mean(), 2))

            with col7:
                st.metric(label='**:blue[Total Retail Orders]**',
                          value='{:,}'.format(df_year[df_year['year'] == year]['total_retail_orders'].sum()))

                st.metric(label='**:blue[Retail Order Growth (%)]**',
                          value=round(df_year[df_year['year'] == year]['growth_retail_orders'].mean(), 2))

            st.divider()

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
