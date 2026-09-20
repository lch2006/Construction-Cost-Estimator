import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title='BuildCost | Construction Cost Estimator', page_icon='🏗️', layout='wide')

st.markdown('''
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem;}
[data-testid="stMetric"] {background: rgba(120,120,120,.08); border: 1px solid rgba(120,120,120,.18); padding: 18px; border-radius: 14px;}
.hero {padding: 22px 26px; border-radius: 18px; background: linear-gradient(135deg,#18222f,#31455d); color:white; margin-bottom: 22px;}
.hero h1 {margin:0; font-size:2.2rem;} .hero p {margin:.35rem 0 0; opacity:.85;}
</style>
''', unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🏗️ BuildCost</h1><p>Construction Cost Estimator • Plan quantities, pricing, markups, and total project cost.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header('Project Settings')
    project_name = st.text_input('Project name', 'Residential Site Development')
    client = st.text_input('Client', 'Example Client')
    location = st.text_input('Project location', 'Blacksburg, VA')
    st.divider()
    contingency = st.number_input('Contingency (%)', 0.0, 100.0, 10.0, 0.5)
    overhead = st.number_input('Overhead (%)', 0.0, 100.0, 5.0, 0.5)
    profit = st.number_input('Profit (%)', 0.0, 100.0, 8.0, 0.5)

st.subheader(project_name)
st.caption(f'{client} • {location}')

if 'items' not in st.session_state:
    st.session_state.items = pd.DataFrame([
        ['Earthwork','Excavation',800.0,'CY',12.50],
        ['Concrete','Concrete',120.0,'CY',165.00],
        ['Paving','Asphalt',500.0,'TON',95.00],
        ['Utilities','Storm Pipe',600.0,'LF',42.00],
        ['Utilities','Sanitary Sewer Pipe',350.0,'LF',55.00],
        ['Site','Curb & Gutter',900.0,'LF',24.00],
    ], columns=['Category','Item','Quantity','Unit','Unit Cost ($)'])

st.markdown('### Estimate Items')
st.caption('Edit cells directly. Add or delete rows using the table controls.')
# Make sure table columns have consistent data types
st.session_state.items["Item"] = st.session_state.items["Item"].astype(str)
st.session_state.items["Category"] = st.session_state.items["Category"].astype(str)
st.session_state.items["Unit"] = st.session_state.items["Unit"].astype(str)

st.session_state.items["Quantity"] = pd.to_numeric(
    st.session_state.items["Quantity"], errors="coerce"
).fillna(0.0)

st.session_state.items["Unit Cost"] = pd.to_numeric(
    st.session_state.items["Unit Cost"], errors="coerce"
).fillna(0.0)
edited = st.data_editor(
    st.session_state.items,
    num_rows='dynamic',
    use_container_width=True,
    hide_index=True,
    column_config={
        'Quantity': st.column_config.NumberColumn(min_value=0.0, format='%.2f'),
        'Unit Cost ($)': st.column_config.NumberColumn(min_value=0.0, format='$%.2f'),
    },
    key='cost_editor'
)
st.session_state.items = edited

df = edited.copy()
for c in ['Quantity','Unit Cost ($)']:
    df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
df['Total Cost'] = df['Quantity'] * df['Unit Cost ($)']

direct = df['Total Cost'].sum()
cont_cost = direct * contingency/100
overhead_cost = direct * overhead/100
base_with_markup = direct + cont_cost + overhead_cost
profit_cost = base_with_markup * profit/100
grand_total = base_with_markup + profit_cost

st.markdown('### Project Summary')
a,b,c,d = st.columns(4)
a.metric('Direct Cost', f'${direct:,.2f}')
b.metric('Contingency', f'${cont_cost:,.2f}', f'{contingency:.1f}%')
c.metric('Overhead', f'${overhead_cost:,.2f}', f'{overhead:.1f}%')
d.metric('Estimated Total', f'${grand_total:,.2f}')

left, right = st.columns([1.25,1])
with left:
    st.markdown('### Cost Breakdown')
    if not df.empty and direct > 0:
        category = df.groupby('Category', dropna=False)['Total Cost'].sum().reset_index()
        category['Category'] = category['Category'].fillna('Uncategorized')
        fig = px.bar(category.sort_values('Total Cost', ascending=False), x='Category', y='Total Cost', text_auto='.2s')
        fig.update_layout(yaxis_title='Cost ($)', xaxis_title='', margin=dict(l=10,r=10,t=10,b=10), height=390)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info('Add estimate items to generate a chart.')

with right:
    st.markdown('### Estimate Details')
    st.dataframe(df[['Category','Item','Quantity','Unit','Unit Cost ($)','Total Cost']], use_container_width=True, hide_index=True,
                 column_config={'Unit Cost ($)': st.column_config.NumberColumn(format='$%.2f'), 'Total Cost': st.column_config.NumberColumn(format='$%.2f')})

st.markdown('### Export')
export = df.copy()
summary = pd.DataFrame({
    'Description':['Direct Cost',f'Contingency ({contingency:.1f}%)',f'Overhead ({overhead:.1f}%)',f'Profit ({profit:.1f}%)','Estimated Total'],
    'Amount':[direct,cont_cost,overhead_cost,profit_cost,grand_total]
})

csv = export.to_csv(index=False).encode('utf-8')
st.download_button('⬇️ Download Estimate CSV', csv, file_name='construction_estimate.csv', mime='text/csv')

st.caption('BuildCost v1.0 • Unit costs are user-provided estimates and should be verified for the specific project, location, and date.')
