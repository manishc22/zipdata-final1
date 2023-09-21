import streamlit as st

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
st.markdown('#### 1. Context')
st.write('This demo app is for CFO / Leadership of a (dummy) Furniture Retail company which has 18 Outlets across India, and also sell their Products (three types of Sofas) across India. The app uses dummy data programmatically created for years 2021-2022.')
st.write('Also, it is assumed that the Organization is split into "States" each of which works like a BU.')
st.divider()
st.markdown('#### 2. Navigation')
st.write('There are 4 Workspaces created in this Demo Data App (other than a Management Reporting Workspace which has been separately created. These Workspaces are around 4 key activities of this (dummy) Retail Company - to check Sales Performance, Product Analysis, Retail / Store Performance, and finally, analyze Product Returns.)')
st.write(
    'These can be navigated via the top right corner Burger Menu icon.)')
st.divider()
st.markdown('#### 3. Constraints in the Demo version')
st.markdown('* All data is dummy')
st.markdown('* Data is only for years 2021-2022')
st.markdown('* Data / Company is assumed to be operating *only* in India, hence the use of Indian currency / names')
st.divider()
st.markdown('#### 4. Next Steps')
st.write('Write to **manish@zipdata.ai** for discussing how we can create a custom Data App best suited for your requirements.')
st.divider()
