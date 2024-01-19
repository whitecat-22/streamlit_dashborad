import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st

df = pd.read_csv('./data/data.csv', encoding='cp932')

# スクリーン全体を使ってグラフが表示されるように設定する
st.set_page_config(layout="wide")

# Layout (Sidebar)
st.sidebar.markdown("## 設定")

division_selected = st.sidebar.multiselect("部署", options=df["division"].unique(), default=df["division"].unique())
period_selected = st.sidebar.selectbox("決算期", df["accounting_period"].unique())

st.header(f"売上・粗利＿{period_selected}期")

# Categorical Variable Bar Chart in Content
df1 = df.query("division == @division_selected & accounting_period == @period_selected")
df1 = df1.groupby(["id", "division", "accounting_period", "class"]).sum(numeric_only=True).reset_index()

# Layout (Content)
df2 = df1[df1["class"].isin(["budget"])]  # 予算
df3 = df1[df1["class"].isin(["result"])]  # 実績（予定）

st.subheader("通期（実績）")
for i, row in df3.iterrows():
    # 5カラム表示
    col1, col2, col3, col4 = st.columns([1,2,2,2])
    # 部署
    division = df3["division"]
    col1.metric("部署", f'{division[i]}')
    # 売上
    sales = df3["sales"][i].sum()
    col2.metric("売上", f'{sales:,.0f}円')
    # 原価
    # costs = df3["costs"][i].sum()-df3["costs2"][i].sum()
    # col2.metric("原価", f'{costs:,.0f}円')
    # 粗利
    profits = df3["profits"][i].sum()-df3["costs2"][i].sum()
    col3.metric("粗利", f'{profits:,.0f}円')
    # 粗利率
    profits_ratio = (profits / sales) * 100
    col4.metric("粗利率", f"{profits_ratio:,.2f}％")

# 売上
fig_sales = go.Figure(data=[
    go.Bar(name="予算", x=df2["division"], y=df2["sales"]),
    go.Bar(name="実績", x=df3["division"], y=df3["sales"]),
])
fig_sales.update_layout(
    height=300,
    width=600,
    margin={'l': 20, 'r': 20, 't': 0, 'b': 0},
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99,
    ),
    barmode='group',
)  # barmode='stack')
fig_sales.update_xaxes(title_text="部署")
fig_sales.update_yaxes(title_text="金額")

# 粗利
fig_profits = go.Figure(data=[
    go.Bar(name="予算", x=df2["division"], y=df2["profits"]),
    go.Bar(name="実績", x=df3["division"], y=df3["profits"]),
])
fig_profits.update_layout(
    height=300,
    width=600,
    margin={'l': 20, 'r': 20, 't': 0, 'b': 0},
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99,
    ),
    barmode='group',
)  # barmode='stack')
fig_profits.update_xaxes(title_text="部署")
fig_profits.update_yaxes(title_text="金額")

# 2カラム表示
left_column, right_column = st.columns([1,1])
left_column.subheader("売上")
left_column.plotly_chart(fig_sales)

right_column.subheader("粗利")
right_column.plotly_chart(fig_profits)
