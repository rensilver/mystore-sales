import pandas as pd
import plotly.express as px
import streamlit as st

from sqlalchemy import create_engine

# =========================
# MYSQL CONNECTION
# =========================

@st.cache_resource
def get_engine():
    db = st.secrets["mysql"]

    connection_string = (
        f"mysql+pymysql://{db['user']}:{db['password']}"
        f"@{db['host']}:{db['port']}/{db['database']}"
    )

    return create_engine(connection_string)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    layout="wide",
    page_icon="📊"
)

# =========================
# CACHE DATA (IMPORTANT)
# =========================
@st.cache_data
def load_orders_data():
    query_orders = "SELECT * FROM orders"

    engine = get_engine()

    return pd.read_sql(query_orders, engine)

@st.cache_data
def load_shopping_data():
    query_shopping = "SELECT * FROM shopping"

    engine = get_engine()

    return pd.read_sql(query_shopping, engine)


df_orders = load_orders_data()
df_shopping = load_shopping_data()

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚙️ Controls")

dark_mode = st.sidebar.toggle("🌙 Dark Mode", True)

payment_method = st.sidebar.multiselect(
    "Payment Method",
    df_orders["Payment_Method"].unique(),
    default=df_orders["Payment_Method"].unique()
)

date_range = st.sidebar.date_input(
    "Date Range",
    [df_orders["Order_Date"].min(), df_orders["Order_Date"].max()]
)

product = st.sidebar.multiselect(
    "Product",
    df_shopping["Product"].unique(),
    default=df_shopping["Product"].unique()
)

# =========================
# FILTER DATA
# =========================
df_filtered = df_orders[
    (df_orders["Payment_Method"].isin(payment_method)) &
    (df_orders["Order_Date"] >= pd.to_datetime(date_range[0])) &
    (df_orders["Order_Date"] <= pd.to_datetime(date_range[1]))
]

df_filtered_shopping = df_shopping[
    (df_shopping["Product"].isin(product))
]

# =========================
# CSS (REFINED GLASS)
# =========================
def load_css(dark):
    if dark:
        bg_color = "#0e1117"
        text = "white"
        card = "rgba(255,255,255,0.05)"
    else:
        bg_color = "#f5f7fa"
        text = "#111"
        card = "white"

    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text};
    }}

    .card {{
        background: {card};
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }}

    .kpi-value {{
        font-size: 28px;
        font-weight: 600;
    }}

    .kpi-label {{
        font-size: 13px;
        opacity: 0.7;
    }}
    </style>
    """, unsafe_allow_html=True)

load_css(dark_mode)

# =========================
# TITLE
# =========================
st.title("📊 Sales Analytics Dashboard")
st.caption("Interactive sales performance overview")

# =========================
# KPI CALCULATIONS
# =========================
total_revenue = df_filtered["Total"].sum()
orders = df_filtered["Id"].nunique()
avg_ticket = df_filtered["Total"].mean()

# Previous period (for delta)
prev_df = df_orders[
    (df_orders["Payment_Method"].isin(payment_method)) &
    (df_orders["Order_Date"] < pd.to_datetime(date_range[0]))
]

prev_revenue = prev_df["Total"].sum()

delta = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0

# =========================
# KPI DISPLAY
# =========================
col1, col2, col3 = st.columns(3)

def kpi(title, value, delta=None):
    delta_html = f"<br><span style='color:lightgreen'>▲ {delta:.1f}%</span>" if delta else ""
    return f"""
    <div class="card">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{title}</div>
        {delta_html}
    </div>
    """

col1.markdown(kpi("Revenue", f"R$ {total_revenue:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), delta), unsafe_allow_html=True)
col2.markdown(kpi("Orders", orders), unsafe_allow_html=True)
col3.markdown(kpi("Avg Ticket", f"R$ {avg_ticket:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")), unsafe_allow_html=True)

# =========================
# CHARTS
# =========================
template = "plotly_dark" if dark_mode else "plotly_white"

col1, col2 = st.columns(2)

# Time series
time_series = (
    df_filtered
    .groupby("Order_Date")["Total"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    time_series,
    x="Order_Date",
    y="Total",
    markers=True,
    title="Revenue Over Time"
)

fig1.update_layout(template=template)

col1.plotly_chart(fig1, width='stretch')

# Top products
top_products = (
    df_filtered_shopping
    .groupby("Product")["Price"]
    .sum()
    .reset_index()
    .sort_values(by="Price", ascending=False)
)

fig2 = px.bar(
    top_products,
    x="Product",
    y="Price",
    text_auto=True,
    title="Top Products"
)

fig2.update_layout(template=template)

col2.plotly_chart(fig2, width='stretch')

# =========================
# DATA TABLE
# =========================
st.subheader("📋 Data")
df_filtered.drop(columns=["customer_id"], inplace=True)
df_filtered["Order_Date"] = pd.to_datetime(df_filtered["Order_Date"])

st.dataframe(
    df_filtered.style.format({
        "Order_Date": lambda x: x.strftime("%d/%m/%Y %H:%M"),
        "Discount": lambda x: f"{x:.2%}".replace(".", ","),
        "Subtotal": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        "Total": lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
    }),
    width='stretch'
)

# =========================
# EMPTY STATE
# =========================
if df_filtered.empty or df_filtered_shopping.empty:
    st.warning("No data available for selected filters.")