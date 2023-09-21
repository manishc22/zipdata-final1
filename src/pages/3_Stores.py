import streamlit.components.v1 as components
import datetime as dt
from datetime import date, time
import datapane as dp
import altair as alt
import pandas as pd
import streamlit as st
from functions.retail_operations import data
from functions.cumulative_sales.trans_tables import *
from functions.cumulative_sales.feeds_post import *
from functions.cumulative_sales.metadata import *
from functions.cumulative_sales.targets_db import *
from functions.cumulative_sales.alerts_db import *

st.set_page_config(
    page_title="Retail Operations",
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

m_data = data.monthly_store_data().data
m_cumulative_data = data.monthly_store_cumulative_data().data
# print(m_cumulative_data)
q_data = data.quarterly_store_data().data
q_cumulative_data = data.quarterly_store_cumulative_data().data
m_growth = data.monthly_store_growth_data().data
q_growth = data.quarterly_store_growth_data().data

df_m = pd.DataFrame(m_data).sort_values(
    by=['month_id'], ascending=False)

df_m_cum = pd.DataFrame(m_cumulative_data).sort_values(
    by=['month_id'], ascending=False)
df_m_cum['total_pos_sales'] = df_m_cum['total_pos_sales'] / 1000000
df_m_cum['total_returns'] = df_m_cum['total_returns'] / 1000000
df_m_cum['total_expenses'] = df_m_cum['total_expenses'] / 1000000
df_m['total_monthly_sales'] = df_m['total_monthly_sales'] / 1000000
df_m['total_expenses'] = df_m['total_expenses'] / 1000000

df_m_g_cum = pd.DataFrame.from_records(
    m_growth).sort_values(
    by=['month_id'], ascending=False)

df_q = pd.DataFrame(q_data).sort_values(
    by=['quarter_id'], ascending=False)

df_q['total_quarter_sales'] = df_q['total_quarter_sales'] / 1000000
df_q['total_expenses'] = df_q['total_expenses'] / 1000000

df_q_cum = pd.DataFrame(q_cumulative_data).sort_values(
    by=['quarter_id'], ascending=False)

df_m_q_cum = pd.DataFrame.from_records(
    q_growth[0]['q_value']).sort_values(
    by=['quarter_id'], ascending=False)

df_q_g_cum = pd.DataFrame.from_records(
    q_growth[0]['q_value']).sort_values(
    by=['quarter_id'], ascending=False)

df_q_cum['total_retail_sales'] = df_q_cum['total_retail_sales'] / 1000000
df_q_cum['total_q_expenses'] = df_q_cum['total_q_expenses'] / 1000000


with tab1:

    col1, col2, col3, col4 = st.columns([1.75, 0.75, 1, 1.25], gap='large')
    with col1:
        funct_tab2 = st.radio(label="Select a Term",
                              options=['Monthly', 'Quarterly', 'Yearly'], horizontal=True, key='tab2-term')
    with col4:
        option_tab2 = st.selectbox('Select a View', options=['Cumulative Metrics',
                                                             'Leaderboards', 'Low Performers', 'Store - Drilldowns'], key='tab2-views')

    st.divider()

    if funct_tab2 == 'Monthly' and option_tab2 == 'Cumulative Metrics':
        st.markdown('##### Monthly Retail Metrics')
        st.markdown(' ')
        with col2:
            month = st.selectbox(
                'Select Month', options=df_m_cum['month_name'].drop_duplicates(), key='tab2-month')

        col4, col5, col6, col7 = st.columns(4)

        with col4:
            st.metric(label='**:blue[Total Retail Sales (*INR million*)]**',
                      value=round((df_m_cum[df_m_cum['month_name'] == month]
                                  ['total_pos_sales'].sum()), 2),
                      delta=df_m_g_cum[df_m_g_cum['month_name'] == month]['total_pos_sales'].values[0])

            st.metric(label='**:blue[Total Returns (*INR million*)]**',
                      value=round(
                          df_m_cum[df_m_cum['month_name'] == month]['total_returns'].sum(), 2),
                      delta=df_m_g_cum[df_m_g_cum['month_name'] == month]['total_returns'].values[0], delta_color='inverse')
            st.metric(label='**:blue[Average Sales Per Employee (*INR*)]**',
                      value='{:,}'.format(
                          df_m_cum[df_m_cum['month_name'] == month]['avg_sales_per_emp'].sum()),
                      delta=df_m_g_cum[df_m_g_cum['month_name'] == month]['avg_sales_per_emp'].values[0])

        with col5:
            st.metric(label='**:blue[Total Retail Orders (*INR million*)]**',
                      value=round(df_m_cum[df_m_cum['month_name'] == month]
                                  ['total_pos_orders'].sum(), 2),
                      delta=df_m_g_cum[df_m_g_cum['month_name'] == month]['total_pos_orders'].values[0])
            st.metric(label='**:blue[Return Percentage]**',
                      value=round(df_m_cum[df_m_cum['month_name'] == month]
                                  ['return_pct'].sum(), 2),
                      delta=df_m_g_cum[df_m_g_cum['month_name'] == month]['return_pct'].values[0], delta_color='inverse')
            st.metric(label='**:blue[Average Sales Per Sq Ft (*INR*)]**',
                      value='{:,}'.format(
                          df_m_cum[df_m_cum['month_name'] == month]['avg_sales_per_sqft'].sum()),
                      delta=df_m_g_cum[df_m_g_cum['month_name'] == month]['avg_sales_per_sqft'].values[0])
        with col6:
            st.metric(label='**:blue[Average Sales Per Order (*INR*)]**',
                      value='{:,}'.format(
                          df_m_cum[df_m_cum['month_name'] == month]['avg_sales_per_order'].sum()),
                      delta=df_m_g_cum[df_m_g_cum['month_name'] == month]['avg_sales_per_order'].values[0])
            st.metric(label='**:blue[Total Expenses (*INR million*)]**',
                      value=round(df_m_cum[df_m_cum['month_name'] == month]
                                  ['total_expenses'].sum(), 2),
                      delta=df_m_g_cum[df_m_g_cum['month_name'] == month]['total_expenses'].values[0])
            st.metric(label='**:blue[Average Discount (*%*)]**',
                      value='{:,}'.format(
                          df_m_cum[df_m_cum['month_name'] == month]['avg_discount'].sum()),
                      delta=df_m_g_cum[df_m_g_cum['month_name'] == month]['avg_discount'].values[0])

        with col7:
            st.metric(label='**:blue[Average Per Store Sales (*INR*)]**',
                      value='{:,}'.format(
                          df_m_cum[df_m_cum['month_name'] == month]['avg_per_store_sales'].sum()),
                      delta=df_m_g_cum[df_m_g_cum['month_name'] == month]['avg_per_store_sales'].values[0])

            st.metric(label='**:blue[Net Profit (*%*)]**',
                      value=round(df_m_cum[df_m_cum['month_name'] == month]
                                  ['net_profit_pct'].sum(), 2),
                      delta=df_m_g_cum[df_m_g_cum['month_name'] == month]['net_profit_pct'].values[0])
        st.divider()

    if funct_tab2 == 'Quarterly' and option_tab2 == 'Cumulative Metrics':
        st.markdown('##### Quarterly Retail Metrics')
        st.markdown(' ')
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_q_cum['quarter'].drop_duplicates(), key='tab2-quarter')

        col4, col5, col6, col7 = st.columns(4)

        with col4:
            st.metric(label='**:blue[Total Retail Sales (*INR million*)]**',
                      value=round((df_q_cum[df_q_cum['quarter'] == quarter]
                                  ['total_retail_sales'].sum()), 2),
                      delta=df_q_g_cum[df_q_g_cum['quarter'] == quarter]['total_retail_sales'].values[0])

            st.metric(label='**:blue[Average Sales Per Employee (*INR*)]**',
                      value='{:,}'.format(
                          df_q_cum[df_q_cum['quarter'] == quarter]['avg_sales_per_emp'].sum()),
                      delta=df_q_g_cum[df_q_g_cum['quarter'] == quarter]['avg_sales_per_emp'].values[0])
            st.metric(label='**:blue[Average Discount (*%*)]**',
                      value='{:,}'.format(
                          df_q_cum[df_q_cum['quarter'] == quarter]['avg_discount'].sum()),
                      delta=df_q_g_cum[df_q_g_cum['quarter'] == quarter]['avg_discount'].values[0])

        with col5:
            st.metric(label='**:blue[Total Retail Orders (*INR million*)]**',
                      value=round(df_q_cum[df_q_cum['quarter'] == quarter]
                                  ['total_retail_orders'].sum(), 2),
                      delta=df_q_g_cum[df_q_g_cum['quarter'] == quarter]['total_retail_orders'].values[0])

            st.metric(label='**:blue[Average Sales Per Sq Ft (*INR*)]**',
                      value='{:,}'.format(
                          df_q_cum[df_q_cum['quarter'] == quarter]['avg_sales_per_sqft'].sum()),
                      delta=df_q_g_cum[df_q_g_cum['quarter'] == quarter]['avg_sales_per_sqft'].values[0])
        with col6:
            st.metric(label='**:blue[Average Sales Per Order (*INR*)]**',
                      value='{:,}'.format(
                          df_q_cum[df_q_cum['quarter'] == quarter]['avg_sales_per_order'].sum()),
                      delta=df_q_g_cum[df_q_g_cum['quarter'] == quarter]['avg_sales_per_order'].values[0])
            st.metric(label='**:blue[Total Expenses (*INR million*)]**',
                      value=round(df_q_cum[df_q_cum['quarter'] == quarter]
                                  ['total_q_expenses'].sum(), 2),
                      delta=df_q_g_cum[df_q_g_cum['quarter'] == quarter]['total_q_expenses'].values[0])

        with col7:
            st.metric(label='**:blue[Average Per Store Sales (*INR*)]**',
                      value='{:,}'.format(
                          df_q_cum[df_q_cum['quarter'] == quarter]['avg_per_store_sales'].sum()),
                      delta=df_q_g_cum[df_q_g_cum['quarter'] == quarter]['avg_per_store_sales'].values[0])

            st.metric(label='**:blue[Net Profit (*%*)]**',
                      value=round(df_q_cum[df_q_cum['quarter'] == quarter]
                                  ['net_profit_pct'].sum(), 2),
                      delta=df_q_g_cum[df_q_g_cum['quarter'] == quarter]['net_profit_pct'].values[0])
        st.divider()

    if funct_tab2 == 'Monthly' and option_tab2 == 'Leaderboards':
        st.markdown('##### Monthly Leaderboards')
        st.markdown(' ')
        with col2:
            month = st.selectbox(
                'Select Month', options=df_m_cum['month_name'].drop_duplicates(), key='tab2-month')
        col8, col9 = st.columns([1, 4], gap='large')

        with col8:
            df_metric = pd.DataFrame(index=df_m.columns)
            df_metric = df_metric.drop(['store_id',
                                       'store_name', 'month_id', 'month_name'])
            df_metric.loc[:, 'labels'] = ['Total Monthly Sales', 'Total Orders', 'Average Order Quantity',
                                          'Average Discount', 'Total Expenses', 'Sales per Employee', 'Sales per Sq Ft', 'Sales / Expense']

            metric = st.selectbox(
                'Select Metric', options=df_metric['labels'])
            metric_col = df_metric[df_metric['labels'] == metric].index[0]

        with col9:
            if metric not in ('store_id' or 'month_id' or 'month_name'):

                df3 = df_m[df_m['month_name'] == month].sort_values(
                    by=metric_col, ascending=False).head(10)

                # print(df3.columns)

                chart = alt.Chart(df3, title=f'Top 10 Stores by {metric}').mark_bar().encode(
                    x=alt.X('store_name', sort=None, title='Stores'),
                    y=alt.Y(metric_col,
                            title=f'{metric}'),
                )
                st.altair_chart(chart,  use_container_width=True)
        st.divider()

    if funct_tab2 == 'Quarterly' and option_tab2 == 'Leaderboards':
        st.markdown('##### Quarterly Leaderboards')
        st.markdown(' ')
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_q_cum['quarter'].drop_duplicates(), key='tab2-month')
        col8, col9 = st.columns([1, 4], gap='large')

        with col8:
            df_metric = pd.DataFrame(index=df_q.columns)

            df_metric = df_metric.drop(['store_id',
                                       'store_name', 'quarter_id', 'quarter'])
            df_metric.loc[:, 'labels'] = ['Total Quarterly Sales', 'Total Quarterly Orders', 'Average Order Quantity',
                                          'Average Discount', 'Total Expenses', 'Sales per Employee', 'Sales per Sq Ft', 'Sales / Expense']

            metric = st.selectbox(
                'Select Metric', options=df_metric['labels'])
            metric_col = df_metric[df_metric['labels'] == metric].index[0]

        with col9:
            if metric not in ('store_id' or 'quarter_id' or 'quarter'):

                df3 = df_q[df_q['quarter'] == quarter].sort_values(
                    by=metric_col, ascending=False).head(10)

                # print(df3.columns)

                chart = alt.Chart(df3, title=f'Top 10 Stores by {metric}').mark_bar().encode(
                    x=alt.X('store_name', sort=None, title='Stores'),
                    y=alt.Y(metric_col,
                            title=f'{metric}'),
                )
                st.altair_chart(chart,  use_container_width=True)
        st.divider()

    if funct_tab2 == 'Monthly' and option_tab2 == 'Low Performers':
        st.markdown('##### Monthly Low Performers')
        st.markdown(' ')
        with col2:
            month = st.selectbox(
                'Select Month', options=df_m_cum['month_name'].drop_duplicates(), key='tab2-month')
        col8, col9 = st.columns([1, 4], gap='large')

        with col8:
            df_metric = pd.DataFrame(index=df_m.columns)
            df_metric = df_metric.drop(['store_id',
                                       'store_name', 'month_id', 'month_name'])
            df_metric.loc[:, 'labels'] = ['Total Monthly Sales', 'Total Orders', 'Average Order Quantity',
                                          'Average Discount', 'Total Expenses', 'Sales per Employee', 'Sales per Sq Ft', 'Sales / Expense']

            metric = st.selectbox(
                'Select Metric', options=df_metric['labels'])
            metric_col = df_metric[df_metric['labels'] == metric].index[0]

        with col9:
            if metric not in ('store_id' or 'month_id' or 'month_name'):

                df3 = df_m[df_m['month_name'] == month].sort_values(
                    by=metric_col, ascending=False).tail(10)

                # print(df3.columns)

                chart = alt.Chart(df3, title=f'Bottom 10 Stores by {metric}').mark_bar().encode(
                    x=alt.X('store_name', sort=None, title='Stores'),
                    y=alt.Y(metric_col,
                            title=f'{metric}'),
                )
                st.altair_chart(chart,  use_container_width=True)
        st.divider()

    if funct_tab2 == 'Quarterly' and option_tab2 == 'Low Performers':
        st.markdown('##### Quarterly Low Performers')
        st.markdown(' ')
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_q_cum['quarter'].drop_duplicates(), key='tab2-month')
        col8, col9, col10 = st.columns([1, 4], gap='large')

        with col8:
            df_metric = pd.DataFrame(index=df_q.columns)

            df_metric = df_metric.drop(['store_id',
                                       'store_name', 'quarter_id', 'quarter'])
            df_metric.loc[:, 'labels'] = ['Total Quarterly Sales', 'Total Quarterly Orders', 'Average Order Quantity',
                                          'Average Discount', 'Total Expenses', 'Sales per Employee', 'Sales per Sq Ft', 'Sales / Expense']

            metric = st.selectbox(
                'Select Metric', options=df_metric['labels'])
            metric_col = df_metric[df_metric['labels'] == metric].index[0]

        with col9:
            if metric not in ('store_id' or 'quarter_id' or 'quarter'):

                df3 = df_q[df_q['quarter'] == quarter].sort_values(
                    by=metric_col, ascending=False).tail(10)

                # print(df3.columns)

                chart = alt.Chart(df3, title=f'Top 10 Stores by {metric}').mark_bar().encode(
                    x=alt.X('store_name', sort=None, title='Stores'),
                    y=alt.Y(metric_col,
                            title=f'{metric}'),
                )
                st.altair_chart(chart,  use_container_width=True)
        st.divider()

    if funct_tab2 == 'Monthly' and option_tab2 == 'Store - Drilldowns':
        st.markdown('##### Monthly Store Metrics')
        st.markdown(' ')
        with col2:
            month = st.selectbox(
                'Select Month', options=df_m['month_name'].drop_duplicates(), key='tab2-month')

        col8, col9 = st.columns([1, 4], gap='large')

        with col8:

            store_name = st.selectbox(
                'Select Store', options=df_m['store_name'])
        with col9:
            col4, col5, col6 = st.columns(3)
            with col4:
                st.metric(label='**:blue[Total Sales (*INR million*)]**',
                          value=round((df_m[(df_m['month_name'] == month) & (df_m['store_name'] == store_name)]
                                       ['total_monthly_sales'].sum()), 2))

                st.metric(label='**:blue[Average Sales Per Employee (*INR*)]**',
                          value='{:,}'.format(df_m[(df_m['month_name'] == month) & (df_m['store_name'] == store_name)]['salesperemp'].sum()))

                st.metric(label='**:blue[Average Order Quantity (*INR*)]**',
                          value='{:,}'.format(df_m[(df_m['month_name'] == month) & (df_m['store_name'] == store_name)]['avgorderquant'].sum()))
            with col5:
                st.metric(label='**:blue[Total Orders (*INR million*)]**',
                          value=round(df_m[(df_m['month_name'] == month) & (df_m['store_name'] == store_name)]
                                      ['total_orders'], 2))

                st.metric(label='**:blue[Average Sales Per Sq Ft (*INR*)]**',
                          value='{:,}'.format(
                              df_m[(df_m['month_name'] == month) & (df_m['store_name'] == store_name)]['salespersqft'].sum()))

                st.metric(label='**:blue[Sales to Expense Ratio]**',
                          value=round(df_m[(df_m['month_name'] == month) & (df_m['store_name'] == store_name)]
                                      ['salestoexpense'], 2))

            with col6:

                st.metric(label='**:blue[Total Expenses (*INR million*)]**',
                          value=round(df_m[(df_m['month_name'] == month) & (df_m['store_name'] == store_name)]
                                      ['total_expenses'].sum(), 2))
                st.metric(label='**:blue[Average Discount (*%*)]**',
                          value='{:,}'.format(
                              df_m[(df_m['month_name'] == month) & (df_m['store_name'] == store_name)]['average_discount'].sum()))

            st.divider()

    if funct_tab2 == 'Quarterly' and option_tab2 == 'Store - Drilldowns':
        st.markdown('##### Quarterly Store Metrics')
        st.markdown(' ')
        with col2:
            quarter = st.selectbox(
                'Select Quarter', options=df_q['quarter'].drop_duplicates(), key='tab2-month')

        col8, col9 = st.columns([1, 4], gap='large')

        with col8:

            store_name = st.selectbox(
                'Select Store', options=df_q['store_name'])
        with col9:
            col4, col5, col6 = st.columns(3)
            with col4:
                st.metric(label='**:blue[Total Sales (*INR million*)]**',
                          value=round((df_q[(df_q['quarter'] == quarter) & (df_q['store_name'] == store_name)]
                                       ['total_quarter_sales'].sum()), 2))

                st.metric(label='**:blue[Average Sales Per Employee (*INR*)]**',
                          value='{:,}'.format(df_q[(df_q['quarter'] == quarter) & (df_q['store_name'] == store_name)]['salesperemp'].sum()))

                st.metric(label='**:blue[Average Order Quantity (*INR*)]**',
                          value='{:,}'.format(df_q[(df_q['quarter'] == quarter) & (df_q['store_name'] == store_name)]['avgorderquant'].sum()))
            with col5:
                st.metric(label='**:blue[Total Orders (*INR million*)]**',
                          value=round(df_q[(df_q['quarter'] == quarter) & (df_q['store_name'] == store_name)]
                                      ['total_quarter_orders'], 2))

                st.metric(label='**:blue[Average Sales Per Sq Ft (*INR*)]**',
                          value='{:,}'.format(
                              df_q[(df_q['quarter'] == quarter) & (df_q['store_name'] == store_name)]['salespersqft'].sum()))

                st.metric(label='**:blue[Sales to Expense Ratio]**',
                          value=round(df_q[(df_q['quarter'] == quarter) & (df_q['store_name'] == store_name)]
                                      ['salestoexpense'], 2))

            with col6:

                st.metric(label='**:blue[Total Expenses (*INR million*)]**',
                          value=round(df_q[(df_q['quarter'] == quarter) & (df_q['store_name'] == store_name)]
                                      ['total_expenses'].sum(), 2))
                st.metric(label='**:blue[Average Discount (*%*)]**',
                          value='{:,}'.format(
                              df_q[(df_q['quarter'] == quarter) & (df_q['store_name'] == store_name)]['average_discount'].sum()))

            st.divider()

with tab2:

    workspace = 'Retail Operations'
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1.5, 1])

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
