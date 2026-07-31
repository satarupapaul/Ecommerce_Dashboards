import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from database import get_connection, create_user, login_user


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Fashion E-Commerce Dashboard",
    page_icon="👗",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sub-title {
        font-size: 17px;
        color: #888888;
        margin-bottom: 25px;
    }

    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.10);
        padding: 20px;
        border-radius: 15px;
    }

    div[data-testid="stMetric"]:hover {
        border: 1px solid rgba(255, 255, 255, 0.30);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# INITIALIZE LOGIN SESSION
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""


# ==================================================
# LOGIN AND SIGN UP PAGE
# ==================================================

if not st.session_state.logged_in:

    st.title("👗 Fashion Analytics")

    menu = st.selectbox(
        "Select Option",
        ["Login", "Sign Up"]
    )


    # --------------------------------------------------
    # LOGIN
    # --------------------------------------------------

    if menu == "Login":

        st.subheader("Login to Your Account")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if email and password:

                user = login_user(email, password)

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user_name = user[1]

                    st.success("Login Successful!")

                    st.rerun()

                else:

                    st.error("Invalid Email or Password")

            else:

                st.warning(
                    "Please enter email and password."
                )


    # --------------------------------------------------
    # SIGN UP
    # --------------------------------------------------

    else:

        st.subheader("Create New Account")

        full_name = st.text_input("Full Name")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Sign Up"):

            if full_name and email and password:

                result = create_user(
                    full_name,
                    email,
                    password
                )

                if result:

                    st.success(
                        "Account created successfully! Please login."
                    )

                else:

                    st.error(
                        "An account with this email already exists."
                    )

            else:

                st.warning("Please fill all fields.")

    st.stop()


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("👗 Fashion Analytics")

st.sidebar.write(
    f"Welcome, {st.session_state.user_name}!"
)

st.sidebar.divider()


page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Sales Analytics",
        "Product Analytics",
        "Dataset Viewer"
    ]
)


st.sidebar.divider()


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False
    st.session_state.user_name = ""

    st.rerun()


# ==================================================
# LOAD DATA FROM MYSQL
# ==================================================

connection = get_connection()


query = """
SELECT *
FROM fashion_sales_data
"""


raw_df = pd.read_sql(
    query,
    connection
)


connection.close()


# ==================================================
# DATA CLEANING USING PANDAS
# ==================================================

sales_df = raw_df[
    raw_df["order_status"] != "Cancelled"
].copy()


# ==================================================
# DASHBOARD PAGE
# ==================================================

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">👗 Fashion Analytics Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sub-title">
        E-Commerce Sales Intelligence using CSV,
        Pandas, NumPy and MySQL
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # DASHBOARD FILTERS
    # --------------------------------------------------

    st.subheader("🔍 Dashboard Filters")


    filter_col1, filter_col2, filter_col3 = st.columns(3)


    with filter_col1:

        selected_city = st.selectbox(
            "Select City",
            ["All"] +
            sorted(
                sales_df["city"].unique().tolist()
            )
        )


    with filter_col2:

        selected_category = st.selectbox(
            "Select Category",
            ["All"] +
            sorted(
                sales_df["category"].unique().tolist()
            )
        )


    with filter_col3:

        selected_brand = st.selectbox(
            "Select Brand",
            ["All"] +
            sorted(
                sales_df["brand"].unique().tolist()
            )
        )


    # --------------------------------------------------
    # APPLY FILTERS
    # --------------------------------------------------

    filtered_df = sales_df.copy()


    if selected_city != "All":

        filtered_df = filtered_df[
            filtered_df["city"] == selected_city
        ]


    if selected_category != "All":

        filtered_df = filtered_df[
            filtered_df["category"]
            == selected_category
        ]


    if selected_brand != "All":

        filtered_df = filtered_df[
            filtered_df["brand"]
            == selected_brand
        ]


    st.divider()


    # --------------------------------------------------
    # NUMPY CALCULATIONS
    # --------------------------------------------------

    sales_array = filtered_df[
        "total_sales"
    ].to_numpy()


    if len(sales_array) > 0:

        total_revenue = np.sum(sales_array)

        average_sale = np.mean(sales_array)

        highest_sale = np.max(sales_array)

        total_quantity = np.sum(
            filtered_df["quantity"].to_numpy()
        )

    else:

        total_revenue = 0
        average_sale = 0
        highest_sale = 0
        total_quantity = 0


    # --------------------------------------------------
    # DASHBOARD METRICS
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "💰 Total Revenue",
        f"₹{total_revenue:,.0f}"
    )


    col2.metric(
        "🛍️ Products Sold",
        f"{total_quantity:,}"
    )


    col3.metric(
        "📊 Average Sale",
        f"₹{average_sale:,.0f}"
    )


    col4.metric(
        "🏆 Highest Sale",
        f"₹{highest_sale:,.0f}"
    )


    st.divider()


    # --------------------------------------------------
    # DASHBOARD CHART ROW 1
    # --------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)


    with chart_col1:

        st.subheader("🏆 Top Selling Products")


        product_sales = (
            filtered_df
            .groupby("product_name")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )


        product_chart = px.bar(
            product_sales,
            x="total_sales",
            y="product_name",
            orientation="h",
            title="Top 10 Products by Revenue"
        )


        product_chart.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            }
        )


        st.plotly_chart(
            product_chart,
            width="stretch"
        )


    with chart_col2:

        st.subheader("🏷️ Category Performance")


        category_sales = (
            filtered_df
            .groupby("category")["total_sales"]
            .sum()
            .reset_index()
        )


        category_chart = px.pie(
            category_sales,
            names="category",
            values="total_sales",
            hole=0.45,
            title="Revenue Distribution by Category"
        )


        st.plotly_chart(
            category_chart,
            width="stretch"
        )


    st.divider()


    # --------------------------------------------------
    # DASHBOARD CHART ROW 2
    # --------------------------------------------------

    chart_col3, chart_col4 = st.columns(2)


    with chart_col3:

        st.subheader("🏢 Brand Performance")


        brand_sales = (
            filtered_df
            .groupby("brand")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )


        brand_chart = px.bar(
            brand_sales,
            x="brand",
            y="total_sales",
            title="Revenue by Brand"
        )


        st.plotly_chart(
            brand_chart,
            width="stretch"
        )


    with chart_col4:

        st.subheader("🌍 City Performance")


        city_sales = (
            filtered_df
            .groupby("city")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )


        city_chart = px.bar(
            city_sales,
            x="city",
            y="total_sales",
            title="Revenue by City"
        )


        st.plotly_chart(
            city_chart,
            width="stretch"
        )


    st.divider()


    # --------------------------------------------------
    # DASHBOARD DATA
    # --------------------------------------------------

    st.subheader("📋 Sales Records")


    st.write(
        f"Displaying {len(filtered_df)} records"
    )


    st.dataframe(
        filtered_df,
        width="stretch"
    )


# ==================================================
# SALES ANALYTICS PAGE
# ==================================================

elif page == "Sales Analytics":

    st.title("📈 Sales Analytics")

    st.write(
        """
        Detailed sales performance and statistical
        analysis using Pandas and NumPy.
        """
    )

    st.divider()


    # --------------------------------------------------
    # NUMPY SALES ANALYSIS
    # --------------------------------------------------

    sales_array = sales_df[
        "total_sales"
    ].to_numpy()


    mean_sales = np.mean(sales_array)

    median_sales = np.median(sales_array)

    std_sales = np.std(sales_array)

    max_sales = np.max(sales_array)


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "📊 Mean Sales",
        f"₹{mean_sales:,.2f}"
    )


    col2.metric(
        "📍 Median Sales",
        f"₹{median_sales:,.2f}"
    )


    col3.metric(
        "📉 Standard Deviation",
        f"₹{std_sales:,.2f}"
    )


    col4.metric(
        "🏆 Maximum Sale",
        f"₹{max_sales:,.2f}"
    )


    st.divider()


    # --------------------------------------------------
    # SALES RANGE FILTER
    # --------------------------------------------------

    st.subheader("🔍 Sales Filter")


    minimum_sale = int(
        sales_df["total_sales"].min()
    )


    maximum_sale = int(
        sales_df["total_sales"].max()
    )


    selected_sales_range = st.slider(
        "Select Sales Range",
        minimum_sale,
        maximum_sale,
        (
            minimum_sale,
            maximum_sale
        )
    )


    filtered_sales = sales_df[
        (
            sales_df["total_sales"]
            >= selected_sales_range[0]
        )
        &
        (
            sales_df["total_sales"]
            <= selected_sales_range[1]
        )
    ]


    st.write(
        f"Records Found: {len(filtered_sales)}"
    )


    st.divider()


    # --------------------------------------------------
    # SALES CHART ROW 1
    # --------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)


    with chart_col1:

        st.subheader("📊 Sales Distribution")


        histogram_chart = px.histogram(
            filtered_sales,
            x="total_sales",
            nbins=20,
            title="Distribution of Sales Amount"
        )


        st.plotly_chart(
            histogram_chart,
            width="stretch"
        )


    with chart_col2:

        st.subheader("📦 Order Status Analysis")


        status_data = (
            filtered_sales
            .groupby("order_status")
            .size()
            .reset_index(name="orders")
        )


        status_chart = px.pie(
            status_data,
            names="order_status",
            values="orders",
            hole=0.45,
            title="Order Status Distribution"
        )


        st.plotly_chart(
            status_chart,
            width="stretch"
        )


    st.divider()


    # --------------------------------------------------
    # SALES CHART ROW 2
    # --------------------------------------------------

    chart_col3, chart_col4 = st.columns(2)


    with chart_col3:

        st.subheader("🌍 Revenue by City")


        city_revenue = (
            filtered_sales
            .groupby("city")["total_sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )


        city_chart = px.bar(
            city_revenue,
            x="city",
            y="total_sales",
            title="City-wise Revenue"
        )


        st.plotly_chart(
            city_chart,
            width="stretch"
        )


    with chart_col4:

        st.subheader("🛍️ Quantity vs Sales")


        scatter_chart = px.scatter(
            filtered_sales,
            x="quantity",
            y="total_sales",
            size="total_sales",
            hover_data=[
                "product_name",
                "category",
                "brand"
            ],
            title="Quantity and Total Sales Relationship"
        )


        st.plotly_chart(
            scatter_chart,
            width="stretch"
        )


    st.divider()


    # --------------------------------------------------
    # PANDAS SALES SUMMARY
    # --------------------------------------------------

    st.subheader("🐼 Pandas Sales Summary")


    sales_summary = (
        filtered_sales
        .groupby("category")
        .agg(
            Total_Revenue=(
                "total_sales",
                "sum"
            ),
            Average_Sale=(
                "total_sales",
                "mean"
            ),
            Total_Quantity=(
                "quantity",
                "sum"
            ),
            Number_of_Orders=(
                "order_id",
                "count"
            )
        )
        .sort_values(
            "Total_Revenue",
            ascending=False
        )
        .reset_index()
    )


    st.dataframe(
        sales_summary,
        width="stretch"
    )


    st.divider()


    # --------------------------------------------------
    # SALES INSIGHTS
    # --------------------------------------------------

    st.subheader("💡 Sales Insights")


    if not filtered_sales.empty:

        best_category = (
            filtered_sales
            .groupby("category")["total_sales"]
            .sum()
            .idxmax()
        )


        best_city = (
            filtered_sales
            .groupby("city")["total_sales"]
            .sum()
            .idxmax()
        )


        best_product = (
            filtered_sales
            .groupby("product_name")["total_sales"]
            .sum()
            .idxmax()
        )


        insight_col1, insight_col2, insight_col3 = (
            st.columns(3)
        )


        insight_col1.success(
            f"🏷️ Best Category: {best_category}"
        )


        insight_col2.success(
            f"🌍 Best City: {best_city}"
        )


        insight_col3.success(
            f"👗 Best Product: {best_product}"
        )


    st.divider()


    st.subheader("📋 Filtered Sales Records")


    st.dataframe(
        filtered_sales,
        width="stretch"
    )


# ==================================================
# PRODUCT ANALYTICS PAGE
# ==================================================

elif page == "Product Analytics":

    st.title("🛍️ Product Analytics")

    st.write(
        """
        Detailed product, category and brand performance
        analysis using Pandas and NumPy.
        """
    )

    st.divider()


    # --------------------------------------------------
    # PRODUCT FILTERS
    # --------------------------------------------------

    st.subheader("🔍 Product Filters")


    filter_col1, filter_col2 = st.columns(2)


    with filter_col1:

        selected_product_category = st.selectbox(
            "Select Product Category",
            ["All"] +
            sorted(
                sales_df["category"].unique().tolist()
            )
        )


    with filter_col2:

        selected_product_brand = st.selectbox(
            "Select Product Brand",
            ["All"] +
            sorted(
                sales_df["brand"].unique().tolist()
            )
        )


    # --------------------------------------------------
    # APPLY PRODUCT FILTERS
    # --------------------------------------------------

    product_filtered_df = sales_df.copy()


    if selected_product_category != "All":

        product_filtered_df = product_filtered_df[
            product_filtered_df["category"]
            == selected_product_category
        ]


    if selected_product_brand != "All":

        product_filtered_df = product_filtered_df[
            product_filtered_df["brand"]
            == selected_product_brand
        ]


    st.divider()


    # --------------------------------------------------
    # PRODUCT SUMMARY USING PANDAS
    # --------------------------------------------------

    product_summary = (
        product_filtered_df
        .groupby("product_name")
        .agg(
            Total_Revenue=(
                "total_sales",
                "sum"
            ),
            Total_Quantity=(
                "quantity",
                "sum"
            ),
            Average_Sale=(
                "total_sales",
                "mean"
            ),
            Number_of_Orders=(
                "order_id",
                "count"
            )
        )
        .sort_values(
            "Total_Revenue",
            ascending=False
        )
        .reset_index()
    )


    # --------------------------------------------------
    # NUMPY PRODUCT CALCULATIONS
    # --------------------------------------------------

    product_revenue_array = (
        product_summary["Total_Revenue"].to_numpy()
    )


    if len(product_revenue_array) > 0:

        total_product_revenue = np.sum(
            product_revenue_array
        )

        average_product_revenue = np.mean(
            product_revenue_array
        )

        highest_product_revenue = np.max(
            product_revenue_array
        )

        total_products = len(product_summary)

    else:

        total_product_revenue = 0
        average_product_revenue = 0
        highest_product_revenue = 0
        total_products = 0


    # --------------------------------------------------
    # PRODUCT METRICS
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "👗 Total Products",
        total_products
    )


    col2.metric(
        "💰 Product Revenue",
        f"₹{total_product_revenue:,.0f}"
    )


    col3.metric(
        "📊 Average Product Revenue",
        f"₹{average_product_revenue:,.0f}"
    )


    col4.metric(
        "🏆 Highest Product Revenue",
        f"₹{highest_product_revenue:,.0f}"
    )


    st.divider()


    # --------------------------------------------------
    # TOP AND BOTTOM PRODUCTS
    # --------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)


    with chart_col1:

        st.subheader("🏆 Top 10 Products")


        top_products = (
            product_summary
            .head(10)
        )


        top_product_chart = px.bar(
            top_products,
            x="Total_Revenue",
            y="product_name",
            orientation="h",
            title="Top 10 Products by Revenue"
        )


        top_product_chart.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            }
        )


        st.plotly_chart(
            top_product_chart,
            width="stretch"
        )


    with chart_col2:

        st.subheader("📉 Bottom 5 Products")


        bottom_products = (
            product_summary
            .tail(5)
            .sort_values("Total_Revenue")
        )


        bottom_product_chart = px.bar(
            bottom_products,
            x="Total_Revenue",
            y="product_name",
            orientation="h",
            title="Bottom 5 Products by Revenue"
        )


        st.plotly_chart(
            bottom_product_chart,
            width="stretch"
        )


    st.divider()


    # --------------------------------------------------
    # BRAND AND CATEGORY ANALYSIS
    # --------------------------------------------------

    chart_col3, chart_col4 = st.columns(2)


    with chart_col3:

        st.subheader("🏢 Brand Analysis")


        brand_analysis = (
            product_filtered_df
            .groupby("brand")
            .agg(
                Revenue=(
                    "total_sales",
                    "sum"
                ),
                Quantity_Sold=(
                    "quantity",
                    "sum"
                )
            )
            .sort_values(
                "Revenue",
                ascending=False
            )
            .reset_index()
        )


        brand_chart = px.bar(
            brand_analysis,
            x="brand",
            y="Revenue",
            hover_data=[
                "Quantity_Sold"
            ],
            title="Revenue Performance by Brand"
        )


        st.plotly_chart(
            brand_chart,
            width="stretch"
        )


    with chart_col4:

        st.subheader("🏷️ Category Analysis")


        category_analysis = (
            product_filtered_df
            .groupby("category")
            .agg(
                Revenue=(
                    "total_sales",
                    "sum"
                ),
                Quantity_Sold=(
                    "quantity",
                    "sum"
                )
            )
            .sort_values(
                "Revenue",
                ascending=False
            )
            .reset_index()
        )


        category_chart = px.pie(
            category_analysis,
            names="category",
            values="Revenue",
            hole=0.45,
            title="Revenue Distribution by Category"
        )


        st.plotly_chart(
            category_chart,
            width="stretch"
        )


    st.divider()


    # --------------------------------------------------
    # QUANTITY ANALYSIS
    # --------------------------------------------------

    st.subheader("🛒 Product Quantity Analysis")


    quantity_analysis = (
        product_filtered_df
        .groupby("product_name")["quantity"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


    quantity_chart = px.bar(
        quantity_analysis,
        x="product_name",
        y="quantity",
        title="Total Quantity Sold by Product"
    )


    st.plotly_chart(
        quantity_chart,
        width="stretch"
    )


    st.divider()


    # --------------------------------------------------
    # PRODUCT INSIGHTS
    # --------------------------------------------------

    st.subheader("💡 Product Insights")


    if not product_summary.empty:

        best_product = (
            product_summary.iloc[0]["product_name"]
        )


        worst_product = (
            product_summary.iloc[-1]["product_name"]
        )


        best_brand = (
            product_filtered_df
            .groupby("brand")["total_sales"]
            .sum()
            .idxmax()
        )


        best_category = (
            product_filtered_df
            .groupby("category")["total_sales"]
            .sum()
            .idxmax()
        )


        insight_col1, insight_col2 = st.columns(2)


        insight_col1.success(
            f"🏆 Highest Revenue Product: {best_product}"
        )


        insight_col2.warning(
            f"📉 Lowest Revenue Product: {worst_product}"
        )


        insight_col3, insight_col4 = st.columns(2)


        insight_col3.info(
            f"🏢 Best Performing Brand: {best_brand}"
        )


        insight_col4.info(
            f"🏷️ Best Performing Category: {best_category}"
        )


    st.divider()


    # --------------------------------------------------
    # PRODUCT RANKING
    # --------------------------------------------------

    st.subheader("🏅 Product Ranking")


    product_summary.insert(
        0,
        "Rank",
        np.arange(
            1,
            len(product_summary) + 1
        )
    )


    st.dataframe(
        product_summary,
        width="stretch"
    )


    st.divider()


    # --------------------------------------------------
    # PRODUCT RECORDS
    # --------------------------------------------------

    st.subheader("📋 Product Sales Records")


    st.write(
        f"Displaying {len(product_filtered_df)} records"
    )


    st.dataframe(
        product_filtered_df,
        width="stretch"
    )


# ==================================================
# DATASET VIEWER PAGE
# ==================================================

elif page == "Dataset Viewer":

    st.title("📂 Dataset Viewer & Data Processing")

    st.write(
        """
        Explore the original Fashion E-Commerce dataset,
        data cleaning process, Pandas analysis, NumPy
        statistics and processed sales data.
        """
    )

    st.divider()


    # --------------------------------------------------
    # DATA PIPELINE INFORMATION
    # --------------------------------------------------

    st.subheader("🔄 Project Data Pipeline")

    st.info(
        """
        CSV Dataset → Pandas Data Loading → Data Cleaning →
        NumPy Statistical Analysis → MySQL Database →
        Streamlit Analytics Dashboard
        """
    )

    st.divider()


    # --------------------------------------------------
    # DATASET OVERVIEW
    # --------------------------------------------------

    st.subheader("📊 Dataset Overview")

    total_rows = raw_df.shape[0]

    total_columns = raw_df.shape[1]

    missing_values = raw_df.isnull().sum().sum()

    duplicate_rows = raw_df.duplicated().sum()


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "📄 Total Records",
        total_rows
    )


    col2.metric(
        "📋 Total Columns",
        total_columns
    )


    col3.metric(
        "❓ Missing Values",
        missing_values
    )


    col4.metric(
        "📑 Duplicate Records",
        duplicate_rows
    )


    st.divider()


    # --------------------------------------------------
    # ORIGINAL DATASET
    # --------------------------------------------------

    st.subheader("📂 Original Dataset")

    st.write(
        """
        The original dataset contains all 500 sales
        records including Delivered, Shipped,
        Processing and Cancelled orders.
        """
    )


    number_of_rows = st.slider(
        "Select Number of Records to Display",
        5,
        len(raw_df),
        20
    )


    st.dataframe(
        raw_df.head(number_of_rows),
        width="stretch"
    )


    st.write(
        f"Showing {number_of_rows} of {len(raw_df)} records."
    )


    st.divider()


    # --------------------------------------------------
    # DATASET COLUMNS
    # --------------------------------------------------

    st.subheader("📋 Dataset Column Information")


    column_information = pd.DataFrame(
        {
            "Column Name": raw_df.columns,

            "Data Type": [
                str(data_type)
                for data_type in raw_df.dtypes
            ],

            "Missing Values": [
                raw_df[column].isnull().sum()
                for column in raw_df.columns
            ],

            "Unique Values": [
                raw_df[column].nunique()
                for column in raw_df.columns
            ]
        }
    )


    st.dataframe(
        column_information,
        width="stretch"
    )


    st.divider()


    # --------------------------------------------------
    # MISSING VALUE ANALYSIS
    # --------------------------------------------------

    st.subheader("❓ Missing Value Analysis")


    missing_data = (
        raw_df
        .isnull()
        .sum()
        .reset_index()
    )


    missing_data.columns = [
        "Column",
        "Missing Values"
    ]


    st.dataframe(
        missing_data,
        width="stretch"
    )


    if missing_values == 0:

        st.success(
            "✅ No missing values found in the dataset."
        )

    else:

        st.warning(
            f"⚠️ Dataset contains {missing_values} missing values."
        )


    st.divider()


    # --------------------------------------------------
    # DUPLICATE ANALYSIS
    # --------------------------------------------------

    st.subheader("📑 Duplicate Record Analysis")


    if duplicate_rows == 0:

        st.success(
            "✅ No duplicate records found in the dataset."
        )

    else:

        st.warning(
            f"⚠️ {duplicate_rows} duplicate records found."
        )


        duplicate_data = raw_df[
            raw_df.duplicated()
        ]


        st.dataframe(
            duplicate_data,
            width="stretch"
        )


    st.divider()


    # --------------------------------------------------
    # PANDAS STATISTICAL SUMMARY
    # --------------------------------------------------

    st.subheader("🐼 Pandas Statistical Summary")

    st.write(
        """
        The Pandas describe() function is used to
        calculate statistical information about
        numerical dataset columns.
        """
    )


    pandas_summary = (
        raw_df
        .describe()
        .transpose()
        .reset_index()
    )


    pandas_summary = pandas_summary.rename(
        columns={
            "index": "Column"
        }
    )


    st.dataframe(
        pandas_summary,
        width="stretch"
    )


    st.divider()


    # --------------------------------------------------
    # NUMPY STATISTICAL ANALYSIS
    # --------------------------------------------------

    st.subheader("🔢 NumPy Statistical Analysis")


    numpy_sales_array = (
        sales_df["total_sales"].to_numpy()
    )


    numpy_mean = np.mean(
        numpy_sales_array
    )


    numpy_median = np.median(
        numpy_sales_array
    )


    numpy_standard_deviation = np.std(
        numpy_sales_array
    )


    numpy_minimum = np.min(
        numpy_sales_array
    )


    numpy_maximum = np.max(
        numpy_sales_array
    )


    numpy_total = np.sum(
        numpy_sales_array
    )


    numpy_col1, numpy_col2, numpy_col3 = (
        st.columns(3)
    )


    numpy_col1.metric(
        "📊 Mean",
        f"₹{numpy_mean:,.2f}"
    )


    numpy_col2.metric(
        "📍 Median",
        f"₹{numpy_median:,.2f}"
    )


    numpy_col3.metric(
        "📉 Standard Deviation",
        f"₹{numpy_standard_deviation:,.2f}"
    )


    numpy_col4, numpy_col5, numpy_col6 = (
        st.columns(3)
    )


    numpy_col4.metric(
        "⬇️ Minimum Sale",
        f"₹{numpy_minimum:,.2f}"
    )


    numpy_col5.metric(
        "⬆️ Maximum Sale",
        f"₹{numpy_maximum:,.2f}"
    )


    numpy_col6.metric(
        "💰 Total Revenue",
        f"₹{numpy_total:,.2f}"
    )


    st.divider()


    # --------------------------------------------------
    # ORDER STATUS ANALYSIS
    # --------------------------------------------------

    st.subheader("📦 Original Order Status Analysis")


    order_status_analysis = (
        raw_df
        .groupby("order_status")
        .size()
        .reset_index(
            name="Number of Orders"
        )
    )


    status_col1, status_col2 = st.columns(2)


    with status_col1:

        st.dataframe(
            order_status_analysis,
            width="stretch"
        )


    with status_col2:

        order_status_chart = px.pie(
            order_status_analysis,
            names="order_status",
            values="Number of Orders",
            hole=0.45,
            title="Original Dataset Order Status"
        )


        st.plotly_chart(
            order_status_chart,
            width="stretch"
        )


    st.divider()


    # --------------------------------------------------
    # DATA CLEANING PROCESS
    # --------------------------------------------------

    st.subheader("🧹 Pandas Data Cleaning Process")


    original_records = len(raw_df)

    cancelled_records = len(
        raw_df[
            raw_df["order_status"] == "Cancelled"
        ]
    )

    valid_records = len(sales_df)


    cleaning_col1, cleaning_col2, cleaning_col3 = (
        st.columns(3)
    )


    cleaning_col1.metric(
        "📂 Original Records",
        original_records
    )


    cleaning_col2.metric(
        "❌ Cancelled Orders Removed",
        cancelled_records
    )


    cleaning_col3.metric(
        "✅ Valid Sales Records",
        valid_records
    )


    st.write(
        """
        Pandas filtering was used to remove cancelled
        orders before performing revenue and product
        analysis.
        """
    )


    st.code(
        '''
sales_df = raw_df[
    raw_df["order_status"] != "Cancelled"
].copy()
        ''',
        language="python"
    )


    st.divider()


    # --------------------------------------------------
    # ORIGINAL VS PROCESSED DATA
    # --------------------------------------------------

    st.subheader("🔄 Original vs Processed Dataset")


    comparison_data = pd.DataFrame(
        {
            "Dataset": [
                "Original Dataset",
                "Processed Dataset"
            ],

            "Number of Records": [
                len(raw_df),
                len(sales_df)
            ]
        }
    )


    comparison_chart = px.bar(
        comparison_data,
        x="Dataset",
        y="Number of Records",
        title="Dataset Records Before and After Cleaning"
    )


    st.plotly_chart(
        comparison_chart,
        width="stretch"
    )


    st.divider()


    # --------------------------------------------------
    # PROCESSED DATASET
    # --------------------------------------------------

    st.subheader("✅ Processed Sales Dataset")


    st.write(
        f"""
        After removing cancelled orders,
        {len(sales_df)} valid sales records remain.
        """
    )


    st.dataframe(
        sales_df,
        width="stretch"
    )


    st.divider()


    # --------------------------------------------------
    # DOWNLOAD DATASET
    # --------------------------------------------------

    st.subheader("⬇️ Download Processed Dataset")


    processed_csv = sales_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="📥 Download Processed CSV",
        data=processed_csv,
        file_name="processed_fashion_sales.csv",
        mime="text/csv"
    )


    st.divider()


    # --------------------------------------------------
    # PROJECT TECHNOLOGIES
    # --------------------------------------------------

    st.subheader("💻 Technologies Used")


    technology_col1, technology_col2 = st.columns(2)


    with technology_col1:

        st.success(
            """
            🐍 Python

            🐼 Pandas

            🔢 NumPy
            """
        )


    with technology_col2:

        st.info(
            """
            🗄️ MySQL

            📊 Plotly

            🌐 Streamlit
            """
        )


    st.divider()


    # --------------------------------------------------
    # FINAL DATA PIPELINE SUMMARY
    # --------------------------------------------------

    st.subheader("🎯 Project Workflow Summary")


    st.write(
        """
        1. A Fashion E-Commerce CSV dataset containing
        500 sales records was created.

        2. Pandas was used to load, inspect, clean and
        analyze the dataset.

        3. NumPy was used to perform mathematical and
        statistical calculations.

        4. The CSV dataset was imported into a MySQL
        database.

        5. Python retrieves the data from MySQL using
        SQL queries.

        6. Streamlit and Plotly are used to create an
        interactive analytics dashboard.

        7. Users can create an account, login, analyze
        sales and products, filter records and download
        the processed dataset.
        """
    )