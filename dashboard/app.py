import plotly.express as px
import streamlit as st

from src.metrics import (
    get_kpis,
    get_monthly_revenue,
    get_regions,
    get_sales_data,
    get_top_products,
)

st.set_page_config(
    page_title="Sales Intelligence",
    page_icon="📊",
    layout="wide",
)

st.title("Sales Intelligence Dashboard")
st.caption(
    "Sales performance analysis using synthetic data. "
    "Revenue includes completed orders only."
)

try:
    regions = get_regions()
    selected_region = st.sidebar.selectbox(
        "Customer region",
        options=["All regions", *regions],
    )
    region_filter = (
        None if selected_region == "All regions" else selected_region
    )

    kpis = get_kpis(region=region_filter)
    monthly = get_monthly_revenue(region=region_filter)
    products = get_top_products(limit=10, region=region_filter)
    sales = get_sales_data(region=region_filter)

except Exception as exc:
    st.error(
        "The database is unavailable. Generate the data and run "
        "the ETL pipeline before opening the dashboard."
    )
    st.exception(exc)
    st.stop()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"R$ {kpis['revenue']:,.2f}")
col2.metric("Completed orders", f"{kpis['total_orders']:,}")
col3.metric("Units sold", f"{kpis['units_sold']:,}")
col4.metric("Average order value", f"R$ {kpis['average_order_value']:,.2f}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Monthly revenue")
    if monthly.empty:
        st.info("No completed sales found for this filter.")
    else:
        figure = px.line(
            monthly,
            x="month",
            y="revenue",
            markers=True,
            title="Revenue over time",
            labels={
                "month": "Month",
                "revenue": "Revenue (R$)",
            },
        )
        st.plotly_chart(figure, use_container_width=True)

with right:
    st.subheader("Top 10 products")
    if not products:
        st.info("No product sales found for this filter.")
    else:
        figure = px.bar(
            products,
            x="units_sold",
            y="product_name",
            orientation="h",
            title="Units sold by product",
            labels={
                "units_sold": "Units sold",
                "product_name": "Product",
            },
        )
        figure.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(figure, use_container_width=True)

st.subheader("Sales data")
st.caption(f"{len(sales):,} completed order records")

if not sales.empty:
    st.dataframe(sales, use_container_width=True, hide_index=True)

    csv_data = sales.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered data (CSV)",
        data=csv_data,
        file_name="sales_data.csv",
        mime="text/csv",
    )
else:
    st.info("No records to display.")