import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from functions.ratio_analysis import data
from functions.utilities.trans_tables import *
from functions.utilities.feeds_post import *
from functions.utilities.metadata import *
from functions.utilities.targets_db import *
from functions.utilities.alerts_db import *

st.set_page_config(
    page_title="Expenses and Budgeting",
    layout="wide"
)

q_ratios = data.quarterly_ratios().data
df_q_ratios = pd.DataFrame.from_records(q_ratios)

tab1, tab2, tab3 = st.tabs(
    ['Dashboard', 'Data Hub', 'Feeds'])

with tab1:
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
