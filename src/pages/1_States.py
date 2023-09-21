import streamlit.components.v1 as components
import datetime as dt
from datetime import date, time

import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import io

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


tab1, tab2, tab3, tab4 = st.tabs(
    ['Dashboard', 'Analysis', 'Budgeting / Planning', 'Feeds'])

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

    col1, col2, col3, col4 = st.columns([1.75, 0.75, 1, 1.25], gap='large')
    with col1:
        funct = st.radio(label="Select a Term",
                         options=['Monthly', 'Quarterly', 'Yearly'], horizontal=True, key='tab1-term')

    option = 'State Drilldown'

    st.divider()

    if funct == 'Monthly' and option == 'State Drilldown':
        with col2:
            month = st.selectbox('Select Month', options=months)
        st.markdown('##### Monthly State Rank & Metrics')
        st.markdown(' ')
        col8, col9 = st.columns([1, 4], gap='large')
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
        col8, col9 = st.columns([1, 4], gap='large')
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

with tab2:
    workspace = 'Cumulative Sales'
    df_exp_budget = pd.read_csv('./files/expense_tbl.csv')
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        state = st.selectbox(
            '*Select State*', options=df_exp_budget['State'].drop_duplicates())

    with col2:
        month = st.selectbox(
            '*Select Month*', options=df_exp_budget['Month'].drop_duplicates())

    with col4:
        view = st.selectbox(
            '*Select a View*', options=['Variance Analysis', 'Set Alerts'])
    st.divider()
    if view == 'Variance Analysis':
        df_selected = df_exp_budget[(df_exp_budget['State'] == state) & (
            df_exp_budget['Month'] == month)][['Territory', 'Quarter', 'Account Name',
                                               'Account Category', 'Cumulative Amount', 'Quarterly Budget']]

        gb = GridOptionsBuilder.from_dataframe(df_selected)

        gb.configure_default_column(
            groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
        # gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_grid_options(domLayout='normal')
        gb.configure_side_bar()
        gridOptions = gb.build()
        # print(df_month.shape)
        # col1, col2, col3 = st.columns([0.5, 8, 0.5], gap='large')
        # with col2:
        st.markdown('##### Variance Analysis')
        grid_response = AgGrid(
            df_selected,
            gridOptions=gridOptions,
            height=400,
            width='100%',
            # data_return_mode=return_mode_value,
            # update_mode=update_mode_value,
            fit_columns_on_grid_load=True,
            # allow_unsafe_jscode=True,  # Set it to True to allow jsfunction to be injected
            enable_enterprise_modules=True
        )

    if view == 'Set Alerts':
        st.markdown(
            '##### Set Alerts for any State / Accounting Code')
        df_targets = pd.DataFrame()
        dataframe, df_targets1 = get_targets(df_targets, workspace)
        df_targets = dataframe

        month_term = target_months(month)
        term = month_term['month_name'].values
        # col1, col2, col3 = st.columns([0.5, 4, 0.5], gap='large')
        # with col2:
        with st.form('Set Alerts'):
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
with tab3:
    df_expenses_quarterly = pd.read_csv('./files/Budget_Quarterly.csv')
    df_expenses_yearly = pd.read_csv('./files/Budget_Yearly.csv')

    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
    with col1:
        term = st.radio('*Select Budget Term*', options=[
                        'Quarterly', 'Yearly'], horizontal=True)
    with col3:
        state = st.selectbox(
            '*Select State*', options=df_expenses_quarterly['State'].drop_duplicates())

    with col4:
        if term == 'Yearly':
            budget = st.selectbox(
                '*Select Year*', options=df_expenses_yearly['Year'].drop_duplicates())
            df_exp_state = df_expenses_yearly[(df_expenses_yearly['State'] == state) & (
                df_expenses_yearly['Year'] == budget)]

        else:
            budget = st.selectbox(
                '*Select Quarter*', options=df_expenses_quarterly['Quarter'].drop_duplicates())
            df_exp_state = df_expenses_quarterly[(df_expenses_quarterly['State'] == state) & (
                df_expenses_quarterly['Quarter'] == budget)]
    st.divider()

    df_exp_state = df_exp_state[['Territory', 'Account Name',
                                 'Account Category', 'Budget']]
    gb = GridOptionsBuilder.from_dataframe(df_exp_state)

    gb.configure_default_column(
        groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
    # gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_grid_options(domLayout='normal')
    gb.configure_side_bar()
    gridOptions = gb.build()
    # print(df_month.shape)
    col1, col2, col3 = st.columns([0.5, 5, 0.5], gap='large')
    with col2:
        st.markdown('##### Budget *(lakhs INR)*')
        grid_response = AgGrid(
            df_exp_state,
            gridOptions=gridOptions,
            height=400,
            width='100%',
            # data_return_mode=return_mode_value,
            # update_mode=update_mode_value,
            fit_columns_on_grid_load=True,
            # allow_unsafe_jscode=True,  # Set it to True to allow jsfunction to be injected
            enable_enterprise_modules=True
        )

        out_df = grid_response["data"]

        # st.write(out_df)

        # def to_excel(df) -> bytes:
        #     output = io.BytesIO()
        #     writer = pd.ExcelWriter(output, engine="xlsxwriter")
        #     df.to_excel(writer, sheet_name="Sheet1")
        #     writer.save()
        #     processed_data = output.getvalue()
        #     return processed_data

        st.button(
            "Submit",

        )


with tab4:
    workspace = 'Cumulative Sales'
    now = dt.date.today()

    min_date = dt.datetime.strptime('01-01-2020', '%m-%d-%Y').date()
    date_value = now.replace(day=1)
    col1, col2, col3, col4, col5 = st.columns([1, 1.5, 4, 1, 1])

    with col1:
        feed_type = st.selectbox(
            '*Feed Type*', options=['All', 'Posts', 'Alerts'])

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
        # link = df_posts.loc[i, 'link']
        link = feed_gen()
        published_at = df_posts.loc[i, 'created_at']
        term = df_posts.loc[i, 'term']
        title = df_posts.loc[i, 'feed_name']
        date, time = published_at.split('T')
        time1, time2 = time.split('.')
        label = f'**{title}**' + '  |   ' + date + ',' + '  ' + time1

        with col2:
            with st.expander(label=label):
                components.html(link, height=600,
                                width=None, scrolling=False)
                # components.iframe(link, height=600,
                #                   width=None, scrolling=False)
        i = i + 1
