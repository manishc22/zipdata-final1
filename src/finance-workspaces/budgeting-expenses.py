import streamlit.components.v1 as components
import datetime as dt
from datetime import date, time
import datapane as dp
import altair as alt
import pandas as pd
import streamlit as st

from functions.budgeting_expenses import data
from functions.utilities.trans_tables import *
from functions.utilities.feeds_post import *
from functions.utilities.metadata import *
from functions.utilities.targets_db import *
from functions.utilities.alerts_db import *

st.set_page_config(
    page_title="Expenses and Budgeting",
    layout="wide"
)

tab1, tab2, tab3 = st.tabs(
    ['Dashboard', 'Data Hub', 'Feeds'])

with tab1:
    m_expenses = data.monthly_total_expenses().data
    df_m_expenses = pd.DataFrame.from_records(
        m_expenses[0]['value'])

    m_cat_expenses = data.monthly_category_expenses().data
    df_m_cat_expenses = pd.DataFrame.from_records(
        m_cat_expenses[0]['value'])

    col1, col2, col3, col4 = st.columns([1.25, 3, 1.75, 0.75])

    with col1:
        option_tab1 = st.selectbox('Select a View', options=['Cumulative Expenses',
                                                             'Category - Trends'], key='tab1-views')

    st.divider()
    if option_tab1 == 'Cumulative Expenses':
        with col3:
            funct_tab1 = st.radio(label="Select a Term",
                                  options=['Monthly', 'Quarterly'], horizontal=True, key='tab1-term')

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
                st.altair_chart(chart,  use_container_width=True)

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
            df_staff.loc[:, 'total_expense'] = df_staff['total_expense'] / 10
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
            df_mktg.loc[:, 'total_expense'] = df_mktg['total_expense'] / 10
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
            df_sal.loc[:, 'total_expense'] = df_sal['total_expense'] / 10
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
            df_taxes.loc[:, 'total_expense'] = df_taxes['total_expense'] / 10
            chart = alt.Chart(df_taxes, title='Tax Expense Trends').mark_line().encode(
                x=alt.X('month_name', sort=None,
                        title='Months'),
                y=alt.Y('total_expense',
                        title='Taxes (in millions)'),
            )
            st.altair_chart(chart,  use_container_width=True)
