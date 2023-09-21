import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import datapane as dp

load_dotenv()


@st.cache_resource
def sql_engine():
    engine = create_engine(
        "postgresql://postgres:o6m7DUBhhoMvYaTJ@db.attmalwrbocsfvwbkmur.supabase.co:6543/postgres")
    return engine


def feed_data():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """SELECT week_id, count(order_id) as total_orders, sum(total_value) as total_Sales, (select w.start_dt from o_weekdays_tbl w where w.id = week_id), (select w.end_dt from o_weekdays_tbl w where w.id = week_id) from t_online_sales_tbl group by week_id order by week_id
               """)
        data = pd.read_sql_query(
            sql, conn)
    return data


def feed_gen():
    data = feed_data()
    total_sales = 0
    total_orders = 0
    change_sales = 0
    change_orders = 0

    value = data.loc[data['week_id'] == 58]['total_sales']/100000
    index = data[data['week_id'] == 58].index[0]
    date_str = str(data.loc[index, 'start_dt']) + \
        ' - ' + str(data.loc[index, 'end_dt'])
    value_1 = round(data.loc[index-1, 'total_sales']/100000, 2)
    order = data.loc[index, 'total_orders']
    order_1 = data.loc[index-1, 'total_orders']
    change_sales = round((value[index] - value_1)*100/value_1, 2)

    if change_sales > 0:
        upward_change_sales = True
    else:
        upward_change_sales = False

    change_orders = round((order - order_1)*100/order_1, 2)

    if change_orders > 0:
        upward_change_order = True
    else:
        upward_change_order = False

    i = index - 4
    while i <= index:
        total_sales = round(data.loc[i, 'total_sales']/100000, 2) + total_sales
        total_orders = data.loc[i, 'total_orders'] + total_orders
        i = i + 1

    average_sales = round(total_sales / 4, 2)
    average_orders = round(total_orders / 4, 1)

    view = dp.Group(
        dp.Text(""" ### Week: {} """.format(date_str)),
        dp.Group(
            dp.BigNumber(
                heading="Total Sales in this week (in lakhs)",
                value=value[index],
                change=change_sales,
                is_upward_change=upward_change_sales,
            ),
            dp.BigNumber(
                heading="Total Sales last week",
                value=value_1,

            ),

            dp.BigNumber(
                heading="Total Orders in this week",
                value=order,
                change=change_orders,
                is_upward_change=upward_change_order,
            ),
            dp.BigNumber(
                heading="Total Orders last week",
                value=order_1,

            ),

            dp.BigNumber(
                heading="Avg Sales last four weeks",
                value=average_sales,
            ),
            dp.BigNumber(
                heading="Average Orders last four weeks",
                value=average_orders,
            ),

            columns=2))
    report = dp.stringify_report(view)
    return report
