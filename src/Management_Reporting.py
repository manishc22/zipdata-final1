from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
import plotly.express as px
import altair as alt
import plotly.graph_objects as go
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import io
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
# data = supabase.table('quarterly_pl').select("*").execute()
# ratios = supabase.table('quarterly_ratios').select("*").execute()


# df = pd.DataFrame(data.data)
# df_ratios = pd.DataFrame(ratios.data)

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')
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
# col1, col2 = st.columns([1, 4])
# st.columns
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ['Sales Performance', 'P & L Trends', 'BS Trends', 'Ratio Analysis', 'Expense Analysis'])

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
        quarterly_data = supabase.table('quarterly_state_performance').select(
            "*").execute()
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

    df_quarter = pd.DataFrame.from_records(
        quarterly_data).sort_values(by=['quarter_id'], ascending=False)

    df_year = pd.DataFrame.from_records(
        yearly_data[0]['y_value']).sort_values(by=['year'], ascending=False)

    df = pd.DataFrame(data.data).dropna(axis=0).sort_values(
        by=['month_id'], ascending=False)

    df['online_sales'] = df['online_sales'] / 1000000
    df['retail_sales'] = df['retail_sales'] / 1000000

    df['year'] = df['month_name'].str.slice(4)

    df_growth = pd.DataFrame(growth_data.data)

    col1, col2, col3, col4 = st.columns([1.75, 0.75, 1, 1.25], gap='large')
    with col1:
        funct = st.radio(label="Select a Term",
                         options=['Monthly', 'Quarterly', 'Yearly'], horizontal=True, key='tab1-term')
    with col4:
        option = st.selectbox('Select a View', options=['Metrics',
                                                        'Sales Leaderboards', 'Risk Analysis', 'Datatables'], key='tab1-views')

    st.divider()

    if funct == 'Monthly' and option == 'Metrics':
        st.markdown('##### Monthly Metrics')
        st.markdown(' ')
        with col2:
            month = st.selectbox(
                'Select Month', options=df['month_name'].drop_duplicates())

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
            month = st.selectbox('Select Month', options=df['month_name'])
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

    if funct == 'Quarterly' and option == 'Metrics':
        st.markdown('##### Quarterly Metrics')
        st.markdown(' ')
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_quarter['quarter'].drop_duplicates())
#         with col2:
        col4, col5, col6, col7 = st.columns(4)
        with col4:
            st.metric(label='**:blue[Total Online Sales (*INR million*)]**',
                      value=df_quarter[(df_quarter['quarter'] == quarter) & (
                          df_quarter['state'] == 'Cumulative')]['online_sales'].values[0],
                      delta=df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] == 'Cumulative')]['growth_online_sales'].values[0])
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
            print(df_quarter.dtypes)
            df_quarter.online_sales = df_quarter.online_sales.astype('float')
            df_quarter.retail_sales = df_quarter.retail_sales.astype('float')
            df_quarter.growth_online_sales = df_quarter.growth_online_sales.astype(
                'float')
            df_quarter.growth_online_orders = df_quarter.growth_online_orders.astype(
                'float')
            df_quarter.growth_retail_sales = df_quarter.growth_online_sales.astype(
                'float')
            df_quarter.growth_retail_orders = df_quarter.growth_retail_orders.astype(
                'float')
            df2 = df_quarter[(df_quarter['quarter'] == quarter) & (df_quarter['state'] != 'Cumulative')].sort_values(
                by='online_sales', ascending=False).head(10)
            df_quarter.online_sales = df2.online_sales.astype('float')
            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df2, title='Top 10 States by Online Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('online_sales',
                        title='Online Sales (in million)')
            )
            st.altair_chart(chart, use_container_width=True)

        with col9:
            df3 = df_quarter[df_quarter['quarter'] == quarter].sort_values(
                by='retail_sales', ascending=False).head(10)

            # st.bar_chart(df2, x='state', y='online_sales')
            chart = alt.Chart(df3, title='Top 10 States by Retail Sales').mark_bar().encode(
                x=alt.X('state', sort=None, title='States'),
                y=alt.Y('retail_sales',
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

    if funct == 'Yearly' and option == 'Metrics':
        st.markdown('##### Yearly Metrics')
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

    if funct == 'Monthly' and option == 'Datatables':
        with col2:
            month = st.selectbox(
                'Select Month', options=df['month_name'].drop_duplicates())
        st.markdown('##### Monthly Data')

        df_month = df[df['month_name'] == month]
        gb = GridOptionsBuilder.from_dataframe(df_month)
        gb.configure_default_column(
            groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
        # gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_grid_options(domLayout='normal')
        gb.configure_side_bar()
        gridOptions = gb.build()
        # print(df_month.shape)
        grid_response = AgGrid(
            df_month,
            gridOptions=gridOptions,
            height=500,
            width='100%',
            # data_return_mode=return_mode_value,
            # update_mode=update_mode_value,
            fit_columns_on_grid_load=True,
            # allow_unsafe_jscode=True,  # Set it to True to allow jsfunction to be injected
            enable_enterprise_modules=True
        )

        out_df = grid_response["data"]

        # st.write(out_df)

        def to_excel(df) -> bytes:
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine="xlsxwriter")
            df.to_excel(writer, sheet_name="Sheet1")
            writer.save()
            processed_data = output.getvalue()
            return processed_data

        st.download_button(
            "Download as excel",
            data=to_excel(out_df),
            file_name="output.xlsx",
            mime="application/vnd.ms-excel",
        )
    if funct == 'Quarterly' and option == 'Datatables':
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_quarter['quarter'].drop_duplicates())
        st.markdown('##### Quarterly Data')
        st.markdown(' ')
        # st.data_editor(df[['state', 'month_name', 'online_sales', 'online_orders', 'retail_sales', 'retail_orders',
        #                    'growth_online_sales', 'growth_online_orders', 'growth_retail_sales', 'growth_retail_orders']], hide_index=True)
        st.data_editor(df_quarter[df_quarter['quarter'] == quarter][['state', 'quarter', 'online_sales', 'online_orders', 'retail_sales', 'retail_orders',
                       'growth_online_sales', 'growth_online_orders', 'growth_retail_sales', 'growth_retail_orders']], hide_index=True)

    if funct == 'Yearly' and option == 'Datatables':
        with col2:
            year = st.selectbox(
                'Select Year', options=df_year['year'].drop_duplicates())
        st.markdown('##### Yearly Data')
        st.markdown(' ')

        st.data_editor(df_year[df_year['year'] == year], hide_index=True)

    if funct == 'Monthly' and option == 'Risk Analysis':
        with col2:
            month = st.selectbox('Select Month', options=df['month_name'])
        st.markdown('##### Monthly Risk Analysis')
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

    if funct == 'Quarterly' and option == 'Risk Analysis':
        df_quarter.online_sales = df_quarter.online_sales.astype('float')
        df_quarter.retail_sales = df_quarter.retail_sales.astype('float')
        df_quarter.growth_online_sales = df_quarter.growth_online_sales.astype(
            'float')
        df_quarter.growth_online_orders = df_quarter.growth_online_orders.astype(
            'float')
        df_quarter.growth_retail_sales = df_quarter.growth_online_sales.astype(
            'float')
        df_quarter.growth_retail_orders = df_quarter.growth_retail_orders.astype(
            'float')
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_quarter['quarter'].drop_duplicates())
        st.markdown('##### Quarterly Risk Analysis')
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

    if funct == 'Yearly' and option == 'Risk Analysis':
        with col2:
            year = st.selectbox(
                'Select Year', options=df_year['year'].drop_duplicates())
        st.markdown('##### Yearly Risk Analysis')
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

    @st.cache_data
    def quarterly_pl():
        data = supabase.table('quarterly_pl').select(
            "*").execute()
        return data

    q_pl = quarterly_pl().data
    df_q_pl = pd.DataFrame.from_records(q_pl)
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

with tab3:

    @st.cache_data
    def quarterly_bs():
        data = supabase.table('quarterly_bs').select(
            "*").execute()
        return data

    q_bs = quarterly_bs().data
    df_q_bs = pd.DataFrame.from_records(q_bs)
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


with tab4:
    @st.cache_data
    def quarterly_ratios():
        data = supabase.table('quarterly_ratios').select(
            "*").execute()
        return data

    q_ratios = quarterly_ratios().data
    df_q_ratios = pd.DataFrame.from_records(q_ratios)

    st.markdown('##### Ratio Analysis & Trends')
    col1, col2 = st.columns(2, gap='large')
    with col1:
        fig1 = go.Figure(data=[
            go.Bar(name='Cash Ratio',
                   x=df_q_ratios['term'], y=df_q_ratios['cash_ratio']),
            go.Bar(name='Quick Ratio',
                   x=df_q_ratios['term'], y=df_q_ratios['quick_ratio']),
            go.Bar(name='Current Ratio',
                   x=df_q_ratios['term'], y=df_q_ratios['current_ratio']),
        ], )
        fig1.update_layout(barmode='group', title="Liquidity Ratios", xaxis_title="Quarters",
                           yaxis_title="Values",
                           legend_title="Ratio Types",)
        st.plotly_chart(fig1, theme='streamlit', use_container_width=True)

        fig3 = go.Figure(data=[
            go.Bar(name='Return on Assets',
                   x=df_q_ratios['term'], y=df_q_ratios['return_on_assets']),
            go.Bar(name='Return on Equity',
                   x=df_q_ratios['term'], y=df_q_ratios['return_on_equity']),
        ], )
        fig3.update_layout(barmode='group', title="ROA / ROE", xaxis_title="Quarters",
                           yaxis_title="Values",
                           legend_title="Ratio Types",)
        st.plotly_chart(fig3, theme='streamlit', use_container_width=True)

        fig4 = go.Figure(data=[
            go.Bar(name='Debt Ratio',
                   x=df_q_ratios['term'], y=df_q_ratios['debt_ratio']),
            go.Bar(name='Debt to Equity Ratio',
                   x=df_q_ratios['term'], y=df_q_ratios['debt_to_equity']),
        ], )
        fig4.update_layout(barmode='group', title="Solvency Ratios", xaxis_title="Quarters",
                           yaxis_title="Values",
                           legend_title="Ratio Types",)
        st.plotly_chart(fig4, theme='streamlit', use_container_width=True)

    with col2:
        fig2 = go.Figure(data=[
            go.Bar(name='Operating Profit Margin',
                   x=df_q_ratios['term'], y=df_q_ratios['operating_profit_margin']),
            go.Bar(name='Gross Margin',
                   x=df_q_ratios['term'], y=df_q_ratios['gross_margin']),
            go.Bar(name='Net Margin',
                   x=df_q_ratios['term'], y=df_q_ratios['net_margin']),
        ], )
        fig2.update_layout(barmode='group', title="Profitability Ratios", xaxis_title="Quarters",
                           yaxis_title="Values",
                           legend_title="Ratio Types",)
        st.plotly_chart(fig2, theme='streamlit', use_container_width=True)

        fig5 = go.Figure(data=[
            go.Bar(name='Asset Turnover Ratio',
                   x=df_q_ratios['term'], y=df_q_ratios['asset_turnover_ratio']),
            go.Bar(name='Equity Turnover Ratio',
                   x=df_q_ratios['term'], y=df_q_ratios['equity_turnover_ratio']),
            go.Bar(name='Payable Turnover Ratio',
                   x=df_q_ratios['term'], y=df_q_ratios['payable_turnover_ratio']),
            go.Bar(name='Inventory Turnover Ratio',
                   x=df_q_ratios['term'], y=df_q_ratios['inventory_turnover_ratio']),
            go.Bar(name='Receivables Turnover Ratio',
                   x=df_q_ratios['term'], y=df_q_ratios['receivables_turnover_ratio']),
        ], )
        fig5.update_layout(barmode='group', title="Efficiency Ratios", xaxis_title="Quarters",
                           yaxis_title="Values",
                           legend_title="Ratio Types",)
        st.plotly_chart(fig5, theme='streamlit', use_container_width=True)

with tab5:
    @st.cache_data
    def monthly_total_expenses():
        data = supabase.table('a_dim_value_tbl').select(
            "value").eq('analysis_id', 24).execute()
        return data

    @st.cache_data
    def monthly_category_expenses():
        data = supabase.table('a_dim_value_tbl').select(
            "value").eq('analysis_id', 25).execute()
        return data

    m_expenses = monthly_total_expenses().data
    df_m_expenses = pd.DataFrame.from_records(
        m_expenses[0]['value'])

    m_cat_expenses = monthly_category_expenses().data
    df_m_cat_expenses = pd.DataFrame.from_records(
        m_cat_expenses[0]['value'])

    col1, col2, col3, col4 = st.columns([1.25, 3, 1.75, 0.75])

    with col1:
        option_tab1 = st.selectbox('Select a View', options=['Cumulative Expenses',
                                                             'Category - Trends'], key='tab5-views')

    st.divider()
    if option_tab1 == 'Cumulative Expenses':
        with col3:
            funct_tab1 = st.radio(label="Select a Term",
                                  options=['Monthly', 'Quarterly'], horizontal=True, key='tab5-term')

        if funct_tab1 == 'Monthly':
            st.markdown('##### Monthly - Expenses')
            with col4:
                month = st.selectbox(
                    'Select Month', options=df_m_expenses['month_name'].drop_duplicates(), index=1)

            col8, col9, col10, col11 = st.columns(4, gap='large')

            with col8:

                st.metric(label='**:blue[Total Monthly Expenses (*INR million*)]**',
                          value=round(
                              (df_m_expenses[(df_m_expenses['month_name'] == month)]['sum'].sum()/10), 2),
                          delta=df_m_expenses[(df_m_expenses['month_name'] == month)]['growth_pct'].mean())

                st.metric(label='**:blue[Salaries, Benefits and Wages]**',
                          value=round(
                              (df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] == 'Salaries, Benefits and Wages')]['total_expense'].sum()/10), 2),
                          delta=df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] == 'Salaries, Benefits and Wages')]['growth'].mean())

            with col9:
                st.metric(label='**:blue[COGS]**',
                          value=round(
                              (df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] == 'Cost of Goods Sold')]['total_expense'].sum()/10), 2),
                          delta=df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] == 'Cost of Goods Sold')]['growth'].mean())

                st.metric(label='**:blue[Other Staff Salaries]**',
                          value=round(
                              (df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] == 'Other Staff Salaries')]['total_expense'].sum()/10), 2),
                          delta=df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] == 'Other Staff Salaries')]['growth'].mean())

            with col10:
                st.metric(label='**:blue[Marketing]**',
                          value=round(
                              (df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] == 'Marketing & Campaigns')]['total_expense'].sum()/10), 2),
                          delta=df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] == 'Marketing & Campaigns')]['growth'].mean())

                st.metric(label='**:blue[Taxes]**',
                          value=round(
                              (df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] == 'Taxes')]['total_expense'].sum()/10), 2),
                          delta=df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] == 'Taxes')]['growth'].mean())

            with col11:
                st.metric(label='**:blue[Other SG&A]**',
                          value=round(
                              (df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] == 'Other SG&A')]['total_expense'].sum()/10), 2),
                          delta=df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] == 'Other SG&A')]['growth'].mean())

            with col10:
                expense_pct = pd.DataFrame(index=[
                    'COGS', 'Marketing & Campaigns', 'Other SG&A', 'Salaries, Benefits & Wages', 'Other Staff Salaries', 'Taxes'], columns=['PCT'])

                # print(expense_pct)
                # print(expense_pct.columns)
                cogs_pct = round((df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] ==
                                                                                                  'Cost of Goods Sold')]['total_expense'].sum())*100/(df_m_expenses[(df_m_expenses['month_name'] == month)]['sum'].sum()), 2)
                mktg_pct = round((df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] ==
                                                                                                  'Marketing & Campaigns')]['total_expense'].sum())*100/(df_m_expenses[(df_m_expenses['month_name'] == month)]['sum'].sum()), 2)
                sga_pct = round((df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] ==
                                'Other SG&A')]['total_expense'].sum())*100/(df_m_expenses[(df_m_expenses['month_name'] == month)]['sum'].sum()), 2)
                wages_pct = round((df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] ==
                                                                                                   'Salaries, Benefits and Wages')]['total_expense'].sum())*100/(df_m_expenses[(df_m_expenses['month_name'] == month)]['sum'].sum()), 2)
                staffsal_pct = round((df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] ==
                                                                                                      'Other Staff Salaries')]['total_expense'].sum())*100/(df_m_expenses[(df_m_expenses['month_name'] == month)]['sum'].sum()), 2)
                taxes_pct = round((df_m_cat_expenses[(df_m_cat_expenses['month_name'] == month) & (df_m_cat_expenses['expense_category'] ==
                                                                                                   'Taxes')]['total_expense'].sum())*100/(df_m_expenses[(df_m_expenses['month_name'] == month)]['sum'].sum()), 2)
                expense_pct.loc['COGS', 'PCT'] = cogs_pct
                expense_pct.loc['Marketing & Campaigns', 'PCT'] = mktg_pct
                expense_pct.loc['Other SG&A', 'PCT'] = sga_pct
                expense_pct.loc['Salaries, Benefits & Wages',
                                'PCT'] = wages_pct
                expense_pct.loc['Other Staff Salaries', 'PCT'] = staffsal_pct
                expense_pct.loc['Taxes', 'PCT'] = taxes_pct
                expense_pct.reset_index(inplace=True)
                expense_pct['PCT'] = expense_pct['PCT'].astype('float')

                expense_pct.sort_values(
                    by='PCT', ascending=False, inplace=True)
                # print(expense_pct)
            st.divider()
            col13, col14 = st.columns(2, gap='large')

            with col13:
                # fig = px.bar(expense_pct, x=expense_pct.index.values,
                #              y="PCT", barmode='stack')
                # st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                # print(expense_pct)
                chart = alt.Chart(expense_pct, title='% Expenses by Category').mark_bar().encode(
                    x=alt.X('PCT',
                            title='% of Total Expenses'),
                    y=alt.Y('index', sort=None,
                            title='Expense Categories'),
                )
                st.altair_chart(chart,  use_container_width=True,)

    if option_tab1 == 'Category - Trends':

        col1, col2 = st.columns(2, gap='large')
        with col1:
            df_cogs = df_m_cat_expenses[df_m_cat_expenses['expense_category']
                                        == 'Cost of Goods Sold']
            df_cogs['total_expense'] = df_cogs['total_expense'] / 10
            # print(df_cogs)
            chart = alt.Chart(df_cogs, title='COGS Trends').mark_line().encode(
                x=alt.X('month_name', sort=None,
                        title='Months'),
                y=alt.Y('total_expense',
                        title='Total COGS Expenses (in millions)'),
            )
            st.altair_chart(chart,  use_container_width=True)

            df_sga = df_m_cat_expenses[df_m_cat_expenses['expense_category']
                                       == 'Other SG&A']
            df_sga['total_expense'] = df_sga['total_expense'] / 10
            # print(df_cogs)
            st.divider()
            st.markdown(' ')
            chart = alt.Chart(df_sga, title='Other SG&A Trends').mark_line().encode(
                x=alt.X('month_name', sort=None,
                        title='Months'),
                y=alt.Y('total_expense',
                        title='Other SGA Expenses (in millions)'),
            )
            st.altair_chart(chart,  use_container_width=True)

            df_staff = df_m_cat_expenses[df_m_cat_expenses['expense_category']
                                         == 'Other Staff Salaries']
            df_staff['total_expense'] = df_staff['total_expense'] / 10
            # print(df_cogs)
            st.divider()
            st.markdown(' ')
            chart = alt.Chart(df_staff, title='Other Staff Salaries').mark_line().encode(
                x=alt.X('month_name', sort=None,
                        title='Months'),
                y=alt.Y('total_expense',
                        title='Other Staff Salaries (in millions)'),
            )
            st.altair_chart(chart,  use_container_width=True)

        with col2:
            df_mktg = df_m_cat_expenses[df_m_cat_expenses['expense_category']
                                        == 'Marketing & Campaigns']
            df_mktg['total_expense'] = df_mktg['total_expense'] / 10
            # print(df_cogs)
            chart = alt.Chart(df_mktg, title='Marketing Expense Trends').mark_line().encode(
                x=alt.X('month_name', sort=None,
                        title='Months'),
                y=alt.Y('total_expense',
                        title='Total Mktg Expenses (in millions)'),
            )
            st.altair_chart(chart,  use_container_width=True)

            st.divider()
            st.markdown(' ')
            df_sal = df_m_cat_expenses[df_m_cat_expenses['expense_category']
                                       == 'Salaries, Benefits and Wages']
            # print(df_sal)
            df_sal['total_expense'] = df_sal['total_expense'] / 10
            chart = alt.Chart(df_sal, title='Salaries, Benefits & Wages Trends').mark_line().encode(
                x=alt.X('month_name', sort=None,
                        title='Months'),
                y=alt.Y('total_expense',
                        title='Sal & Benefits Expenses (in millions)'),
            )
            st.altair_chart(chart,  use_container_width=True)

            st.divider()
            st.markdown(' ')
            df_taxes = df_m_cat_expenses[df_m_cat_expenses['expense_category']
                                         == 'Taxes']
            # print(df_sal)
            df_taxes['total_expense'] = df_taxes['total_expense'] / 10
            chart = alt.Chart(df_taxes, title='Tax Expense Trends').mark_line().encode(
                x=alt.X('month_name', sort=None,
                        title='Months'),
                y=alt.Y('total_expense',
                        title='Taxes (in millions)'),
            )
            st.altair_chart(chart,  use_container_width=True)
