import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st

df = pd.read_csv('./data/data.csv')

# スクリーン全体を使ってグラフが表示されるように設定する
st.set_page_config(layout="wide")

# Layout (Sidebar)
st.sidebar.markdown("## 設定")

division_selected = st.sidebar.selectbox("部署", df["division"].unique())
period_selected = st.sidebar.selectbox("決算期", df["accounting_period"].unique())

st.header(f"売上・粗利＿{division_selected}（{period_selected}期）")

# Categorical Variable Bar Chart in Content
df_ = df.query("division == @division_selected & accounting_period == @period_selected")
df_ = df_.groupby(["division", "accounting_period", "year", "month"]).sum(numeric_only=True).reset_index()

fig_sales = go.Figure(data=[
    go.Bar(name="売上", x=df_["month"], y=df_["sales"]),
])
fig_profits = go.Figure(data=[
    go.Bar(name="粗利", x=df_["month"], y=df_["profits"]),
])

fig_sales.update_layout(height=300,
                      width=1000,
                      margin={'l': 20, 'r': 20, 't': 0, 'b': 0},
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="right",
                          x=0.99),
                      barmode='stack')
fig_sales.update_xaxes(title_text="月")
fig_sales.update_yaxes(title_text="金額")

fig_profits.update_layout(height=300,
                      width=1000,
                      margin={'l': 20, 'r': 20, 't': 0, 'b': 0},
                      legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="right",
                          x=0.99),
                      barmode='stack')
fig_profits.update_xaxes(title_text="月")
fig_profits.update_yaxes(title_text="金額")

# Layout (Content)
#left_column, right_column = st.columns(2)
st.subheader("売上")
st.plotly_chart(fig_sales)

st.subheader("粗利")
st.plotly_chart(fig_profits)
