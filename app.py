"""
================================================================================
DASHBOARD DATA WAREHOUSE - GROCERY SALES ANALYTICS (DARK THEME EDITION)
Teknologi: Streamlit, Plotly, Pandas, SQLAlchemy (MySQL)
Database : grocery_sales_dw (Star Schema)
Tema     : Sleek Dark Mode (Meredakan ketegangan mata, kontras tinggi, modern)
================================================================================
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from sqlalchemy import create_engine

# Set global plotly dark template
pio.templates.default = "plotly_dark"

# ==============================================================================
# 1. PAGE CONFIGURATION & CUSTOM DARK STYLING
# ==============================================================================
st.set_page_config(
    page_title="Grocery Sales DWH Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Sleek Dark Theme (Slate / Cyan / Emerald)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #F8FAFC;
    }
    
    /* Main Background & Sidebar */
    .stApp {
        background-color: #0B1120;
    }
    [data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid #1E293B;
    }
    
    /* Header Gradient Banner */
    .dash-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 55%, #042F2C 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px -5px rgba(0,0,0,0.6);
        border: 1px solid #1E293B;
    }
    .dash-header h1 {
        font-size: 28px;
        font-weight: 800;
        margin: 0;
        color: #38BDF8;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .dash-header p {
        font-size: 14px;
        color: #94A3B8;
        margin: 6px 0 0 0;
    }
    
    /* Dark Mode Metric Cards */
    .kpi-card {
        background: #1E293B;
        border-radius: 14px;
        padding: 20px 22px;
        border: 1px solid #334155;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px -5px rgba(0,0,0,0.5);
        border-color: #38BDF8;
    }
    .kpi-label {
        font-size: 12px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 27px;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.5px;
    }
    .kpi-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        margin-top: 10px;
    }
    .badge-success { background: rgba(16, 185, 129, 0.18); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.35); }
    .badge-info { background: rgba(56, 189, 248, 0.18); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.35); }
    .badge-warning { background: rgba(245, 158, 11, 0.18); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.35); }
    
    /* Tabs Styling - Dark Mode */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1E293B;
        padding: 7px;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 9px 18px;
        font-weight: 600;
        color: #94A3B8;
        border: none;
        background-color: transparent;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #F8FAFC;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0F766E !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 10px rgba(15, 118, 110, 0.4);
    }
    
    /* Plotly Card Container */
    .chart-box {
        background: #1E293B;
        border-radius: 14px;
        padding: 16px;
        border: 1px solid #334155;
        box-shadow: 0 4px 15px rgba(0,0,0,0.25);
        margin-bottom: 20px;
    }
    
    /* Custom Info Callout */
    .info-callout {
        background: rgba(14, 116, 144, 0.15);
        border-left: 4px solid #06B6D4;
        padding: 14px 18px;
        border-radius: 8px;
        color: #E0F2FE;
        font-size: 13.5px;
        margin: 16px 0;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to apply dark layout to any plotly chart
def style_chart(fig, height=380, title=None):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font=dict(family="Plus Jakarta Sans", color="#F1F5F9", size=11),
        title=dict(text=title, font=dict(color="#F8FAFC", size=14, weight="bold")) if title else None,
        margin=dict(l=20, r=20, t=50 if title else 20, b=20),
        height=height,
        xaxis=dict(gridcolor="#334155", zerolinecolor="#475569", linecolor="#475569"),
        yaxis=dict(gridcolor="#334155", zerolinecolor="#475569", linecolor="#475569")
    )
    return fig

# ==============================================================================
# 2. DATA LOADING & CACHING ENGINE
# ==============================================================================
@st.cache_resource(show_spinner=False)
def get_db_engine():
    try:
        engine = create_engine("mysql+pymysql://root:@localhost:3306/grocery_sales_dw")
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return engine
    except Exception as e:
        return None

@st.cache_data(ttl=3600, show_spinner="Memuat Data Warehouse...")
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parquet_path = os.path.join(current_dir, "data", "grocery_sales_dwh.parquet")
    
    # Prioritas 1: High-Speed Parquet DWH Cache (Ideal untuk Cloud 24/7 & Local Instant Load < 0.5s)
    if os.path.exists(parquet_path):
        try:
            df = pd.read_parquet(parquet_path)
            df['Tanggal'] = pd.to_datetime(df['Tanggal'], errors='coerce')
            return df, "Cloud DWH Engine (High-Speed Parquet • 200k Rows)"
        except Exception:
            pass

    # Prioritas 2: Live MySQL DWH jika server MySQL aktif
    engine = get_db_engine()
    if engine is not None:
        try:
            query = """
            SELECT 
                f.FactID,
                f.TransactionNumber,
                w.Tanggal,
                w.Hari,
                w.NamaBulan,
                w.Bulan,
                w.Kuartal,
                w.Tahun,
                p.ProductID,
                p.ProductName,
                p.Price AS UnitPrice,
                p.Class AS PriceClass,
                p.VitalityDays,
                c.CategoryName,
                cu.CustomerID,
                cu.FullName AS CustomerName,
                ci.CityName,
                ci.CountryName,
                e.EmployeeID,
                e.FullName AS EmployeeName,
                e.Gender AS EmployeeGender,
                f.Quantity,
                f.Discount,
                f.TotalPrice
            FROM FactSales f
            JOIN DimWaktu w ON f.WaktuID = w.WaktuID
            JOIN DimProduct p ON f.ProductID = p.ProductID
            JOIN DimCategory c ON f.CategoryID = c.CategoryID
            JOIN DimCustomer cu ON f.CustomerID = cu.CustomerID
            JOIN DimCity ci ON f.CityID = ci.CityID
            JOIN DimEmployee e ON f.EmployeeID = e.EmployeeID
            LIMIT 200000;
            """
            df = pd.read_sql(query, engine)
            df['Tanggal'] = pd.to_datetime(df['Tanggal'], errors='coerce')
            return df, "MySQL Live (grocery_sales_dw)"
        except Exception:
            pass

    # Prioritas 3: Fallback ke cleaned CSV
    clean_csv_path = os.path.join(os.path.dirname(current_dir), "clean_csv")
    if not os.path.exists(clean_csv_path):
        clean_csv_path = r"c:\Users\User\Downloads\Grocery Sistem Ali\clean_csv"
    if os.path.exists(clean_csv_path):
        sales = pd.read_csv(os.path.join(clean_csv_path, "sales.csv"))
        products = pd.read_csv(os.path.join(clean_csv_path, "products.csv"))
        categories = pd.read_csv(os.path.join(clean_csv_path, "categories.csv"))
        customers = pd.read_csv(os.path.join(clean_csv_path, "customers.csv"))
        cities = pd.read_csv(os.path.join(clean_csv_path, "cities.csv"))
        countries = pd.read_csv(os.path.join(clean_csv_path, "countries.csv"))
        employees = pd.read_csv(os.path.join(clean_csv_path, "employees.csv"))
        
        prod = products.merge(categories, on="CategoryID", how="left")
        cust = customers.merge(cities.merge(countries, on="CountryID", how="left"), on="CityID", how="left")
        cust['CustomerName'] = cust['FirstName'] + ' ' + cust['LastName']
        emp = employees.merge(cities, on="CityID", how="left")
        emp['EmployeeName'] = emp['FirstName'] + ' ' + emp['LastName']
        emp = emp.rename(columns={'Gender': 'EmployeeGender'})
        
        df = sales.merge(prod[['ProductID', 'ProductName', 'Price', 'CategoryName', 'Class', 'VitalityDays']], on="ProductID", how="left")
        df = df.rename(columns={'Price': 'UnitPrice', 'Class': 'PriceClass'})
        df = df.merge(cust[['CustomerID', 'CustomerName', 'CityName', 'CountryName']], on="CustomerID", how="left")
        df = df.merge(emp[['EmployeeID', 'EmployeeName', 'EmployeeGender']], left_on="SalesPersonID", right_on="EmployeeID", how="left")
        
        df['Tanggal'] = pd.to_datetime(df['SalesDate'], errors='coerce')
        df['Hari'] = df['Tanggal'].dt.day_name()
        df['NamaBulan'] = df['Tanggal'].dt.month_name()
        df['Bulan'] = df['Tanggal'].dt.month
        df['Kuartal'] = df['Tanggal'].dt.quarter
        df['Tahun'] = df['Tanggal'].dt.year
        df['FactID'] = df['SalesID']
        return df, "Local CSV Fallback (clean_csv)"

    return pd.DataFrame(), "No Data"

df_raw, source_status = load_data()

# ==============================================================================
# 3. SIDEBAR CONTROLS & FILTERS
# ==============================================================================
st.sidebar.image("https://img.icons8.com/fluency/96/shopping-basket.png", width=65)
st.sidebar.markdown("### 🎛️ Filter Analisis")
st.sidebar.markdown(f"<span style='color:#38BDF8; font-size:12px;'>● Live Data Source:</span><br><code style='color:#34D399; font-size:11px;'>{source_status}</code>", unsafe_allow_html=True)
st.sidebar.divider()

if not df_raw.empty:
    min_date = df_raw['Tanggal'].min().date()
    max_date = df_raw['Tanggal'].max().date()
    date_range = st.sidebar.date_input(
        "Rentang Waktu Transaksi:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    all_categories = sorted(df_raw['CategoryName'].dropna().unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Kategori Barang:",
        options=all_categories,
        default=all_categories[:5] if len(all_categories) > 5 else all_categories
    )
    
    all_classes = sorted(df_raw['PriceClass'].dropna().unique().tolist())
    selected_classes = st.sidebar.multiselect(
        "Kelas Harga Produk:",
        options=all_classes,
        default=all_classes
    )
    
    all_cities = sorted(df_raw['CityName'].dropna().unique().tolist())
    selected_cities = st.sidebar.multiselect(
        "Kota Pelanggan:",
        options=all_cities,
        default=[]
    )
    
    discount_filter = st.sidebar.slider(
        "Maksimum Diskon:",
        min_value=0.0,
        max_value=float(df_raw['Discount'].max()),
        value=float(df_raw['Discount'].max()),
        step=0.05,
        format="%.0f%%"
    )

    # Filter evaluation
    df = df_raw.copy()
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['Tanggal'].dt.date >= start_date) & (df['Tanggal'].dt.date <= end_date)]
    if selected_categories:
        df = df[df['CategoryName'].isin(selected_categories)]
    if selected_classes:
        df = df[df['PriceClass'].isin(selected_classes)]
    if selected_cities:
        df = df[df['CityName'].isin(selected_cities)]
    df = df[df['Discount'] <= discount_filter]
else:
    df = pd.DataFrame()

# ==============================================================================
# 4. HEADER BANNER
# ==============================================================================
st.markdown("""
<div class="dash-header">
    <h1>🛒 Grocery Sales Data Warehouse Analytics</h1>
    <p>Executive Business Intelligence Dashboard berbasis Star Schema (Database: <b>grocery_sales_dw</b> | 200.000 Transaksi Terverifikasi)</p>
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.warning("Tidak ada data yang memenuhi kriteria filter saat ini.")
    st.stop()

# ==============================================================================
# 5. KPI SUMMARY CARDS (DARK THEME)
# ==============================================================================
total_revenue = df['TotalPrice'].sum()
total_txns = len(df)
total_units = df['Quantity'].sum()
avg_order_val = total_revenue / total_txns if total_txns > 0 else 0
unique_cust = df['CustomerID'].nunique()
avg_disc = df['Discount'].mean() * 100

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-value">${total_revenue:,.2f}</div>
        <span class="kpi-badge badge-success">💰 Total Penjualan</span>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Transaksi</div>
        <div class="kpi-value">{total_txns:,}</div>
        <span class="kpi-badge badge-info">🛒 Total Order</span>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Unit Terjual</div>
        <div class="kpi-value">{total_units:,}</div>
        <span class="kpi-badge badge-warning">📦 Total Barang</span>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Order Value</div>
        <div class="kpi-value">${avg_order_val:,.2f}</div>
        <span class="kpi-badge badge-info">🏷️ Rata-rata Struk</span>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Pelanggan Aktif</div>
        <div class="kpi-value">{unique_cust:,}</div>
        <span class="kpi-badge badge-success">👥 Total Customer</span>
    </div>
    """, unsafe_allow_html=True)

with c6:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Rata-rata Diskon</div>
        <div class="kpi-value">{avg_disc:.1f}%</div>
        <span class="kpi-badge badge-warning">📉 Tingkat Potongan</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 6. TAB NAVIGATION (DARK THEME)
# ==============================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Executive Overview",
    "🍎 Produk & Kategori",
    "👥 Pelanggan & Geografi",
    "👔 Karyawan Kasir",
    "🏷️ Diskon & Elastisitas",
    "🗄️ Star Schema & Explorer"
])

# ------------------------------------------------------------------------------
# TAB 1: EXECUTIVE OVERVIEW
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("📈 Tren Penjualan dan Volume Transaksi")
    
    col_t1, col_t2 = st.columns([2, 1])
    
    with col_t1:
        monthly = df.groupby(['Tahun', 'Bulan', 'NamaBulan']).agg(
            Revenue=('TotalPrice', 'sum'),
            Transaksi=('FactID', 'count')
        ).reset_index().sort_values(['Tahun', 'Bulan'])
        monthly['Periode'] = monthly['NamaBulan'] + ' ' + monthly['Tahun'].astype(str)
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=monthly['Periode'],
            y=monthly['Revenue'],
            name='Total Revenue ($)',
            marker_color='#14B8A6',
            opacity=0.9
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly['Periode'],
            y=monthly['Transaksi'],
            name='Jumlah Transaksi',
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='#F43F5E', width=3),
            marker=dict(size=8, color='#FDA4AF')
        ))
        fig_trend.update_layout(
            title="Tren Penjualan Bulanan (Revenue vs Jumlah Transaksi)",
            yaxis=dict(title="Revenue ($)", showgrid=True),
            yaxis2=dict(title="Jumlah Transaksi", overlaying='y', side='right', showgrid=False),
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(30,41,59,0.85)'),
            hovermode="x unified"
        )
        style_chart(fig_trend, height=380)
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_t2:
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_sales = df.groupby('Hari')['TotalPrice'].sum().reindex(day_order).reset_index()
        
        fig_day = px.bar(
            day_sales,
            x='Hari',
            y='TotalPrice',
            title="Penjualan Berdasarkan Hari",
            labels={'TotalPrice': 'Revenue ($)', 'Hari': 'Hari Transaksi'},
            color='TotalPrice',
            color_continuous_scale='teal'
        )
        style_chart(fig_day, height=380)
        fig_day.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_day, use_container_width=True)

    # Quarterly Metrics
    st.subheader("📅 Performa Kuartalan (Quarterly Breakdown)")
    quarter_sales = df.groupby('Kuartal').agg(
        Revenue=('TotalPrice', 'sum'),
        Unit=('Quantity', 'sum'),
        Transaksi=('FactID', 'count')
    ).reset_index()
    quarter_sales['Kuartal'] = 'Kuartal ' + quarter_sales['Kuartal'].astype(str)
    
    col_q1, col_q2, col_q3 = st.columns(3)
    for idx, row in quarter_sales.iterrows():
        with [col_q1, col_q2, col_q3][idx % 3]:
            st.metric(
                label=f"📊 {row['Kuartal']}",
                value=f"${row['Revenue']:,.2f}",
                delta=f"{row['Transaksi']:,} Transaksi ({row['Unit']:,} unit)"
            )

# ------------------------------------------------------------------------------
# TAB 2: PRODUCT & CATEGORY ANALYTICS
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("🍎 Analisis Kategori dan Produk Unggulan")
    
    col_p1, col_p2 = st.columns([1.5, 1])
    
    with col_p1:
        cat_rev = df.groupby('CategoryName').agg(
            Revenue=('TotalPrice', 'sum'),
            Unit=('Quantity', 'sum'),
            Transaksi=('FactID', 'count')
        ).reset_index().sort_values('Revenue', ascending=True)
        
        fig_cat = px.bar(
            cat_rev,
            x='Revenue',
            y='CategoryName',
            orientation='h',
            title="Total Revenue per Kategori Produk",
            labels={'Revenue': 'Total Revenue ($)', 'CategoryName': 'Kategori'},
            color='Revenue',
            color_continuous_scale='blugrn',
            text=cat_rev['Revenue'].apply(lambda x: f"${x/1000:,.0f}K")
        )
        style_chart(fig_cat, height=420)
        fig_cat.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_cat, use_container_width=True)
        
    with col_p2:
        class_sales = df.groupby('PriceClass')['TotalPrice'].sum().reset_index()
        fig_class = px.pie(
            class_sales,
            values='TotalPrice',
            names='PriceClass',
            title="Distribusi Penjualan per Kelas Harga",
            hole=0.45,
            color_discrete_sequence=['#14B8A6', '#38BDF8', '#F59E0B']
        )
        style_chart(fig_class, height=420)
        st.plotly_chart(fig_class, use_container_width=True)

    st.subheader("🏆 Top 10 Produk Terlaris (Revenue Terbesar)")
    top_prod = df.groupby(['ProductName', 'CategoryName']).agg(
        Revenue=('TotalPrice', 'sum'),
        Unit=('Quantity', 'sum'),
        Transaksi=('FactID', 'count'),
        HargaSatuan=('UnitPrice', 'mean')
    ).reset_index().sort_values('Revenue', ascending=False).head(10)
    
    fig_top_prod = px.bar(
        top_prod,
        x='ProductName',
        y='Revenue',
        color='CategoryName',
        title="Top 10 Produk dengan Kontribusi Omset Tertinggi",
        labels={'Revenue': 'Total Revenue ($)', 'ProductName': 'Nama Produk', 'CategoryName': 'Kategori'},
        text=top_prod['Revenue'].apply(lambda x: f"${x:,.0f}"),
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    style_chart(fig_top_prod, height=400)
    st.plotly_chart(fig_top_prod, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 3: CUSTOMER & GEOGRAPHY
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("🏙️ Distribusi Geografis & Segmentasi Pelanggan")
    
    col_g1, col_g2 = st.columns([1.5, 1])
    
    with col_g1:
        city_sales = df.groupby(['CityName', 'CountryName']).agg(
            Revenue=('TotalPrice', 'sum'),
            Transaksi=('FactID', 'count'),
            Pelanggan=('CustomerID', 'nunique')
        ).reset_index().sort_values('Revenue', ascending=False).head(10)
        
        fig_city = px.bar(
            city_sales,
            x='CityName',
            y='Revenue',
            color='Revenue',
            color_continuous_scale='viridis',
            title="Top 10 Kota dengan Penjualan Tertinggi",
            labels={'CityName': 'Nama Kota', 'Revenue': 'Total Revenue ($)'},
            text=city_sales['Revenue'].apply(lambda x: f"${x/1000:,.0f}K")
        )
        style_chart(fig_city, height=400)
        fig_city.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_city, use_container_width=True)
        
    with col_g2:
        st.markdown("#### 🌟 Top 10 Pelanggan VIP")
        top_cust = df.groupby(['CustomerID', 'CustomerName', 'CityName']).agg(
            TotalBelanja=('TotalPrice', 'sum'),
            Kunjungan=('FactID', 'count')
        ).reset_index().sort_values('TotalBelanja', ascending=False).head(10)
        
        top_cust['TotalBelanja'] = top_cust['TotalBelanja'].apply(lambda x: f"${x:,.2f}")
        st.dataframe(top_cust, use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# TAB 4: EMPLOYEE PERFORMANCE
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("👔 Peringkat & Performa Karyawan Kasir (Salesperson)")
    
    emp_perf = df.groupby(['EmployeeID', 'EmployeeName', 'EmployeeGender']).agg(
        Revenue=('TotalPrice', 'sum'),
        Unit=('Quantity', 'sum'),
        Transaksi=('FactID', 'count'),
        AvgPerTxn=('TotalPrice', 'mean')
    ).reset_index().sort_values('Revenue', ascending=False)
    
    fig_emp = px.bar(
        emp_perf,
        x='EmployeeName',
        y='Revenue',
        color='EmployeeGender',
        color_discrete_map={'F': '#F43F5E', 'M': '#38BDF8'},
        title="Total Penjualan per Karyawan Kasir",
        labels={'EmployeeName': 'Nama Kasir', 'Revenue': 'Total Penjualan ($)', 'EmployeeGender': 'Gender'},
        text=emp_perf['Revenue'].apply(lambda x: f"${x/1000:,.0f}K")
    )
    style_chart(fig_emp, height=420)
    st.plotly_chart(fig_emp, use_container_width=True)
    
    st.markdown("#### 📋 Papan Peringkat Karyawan Kasir (Leaderboard)")
    emp_table = emp_perf.copy()
    emp_table['Peringkat'] = range(1, len(emp_table) + 1)
    emp_table['Revenue'] = emp_table['Revenue'].apply(lambda x: f"${x:,.2f}")
    emp_table['AvgPerTxn'] = emp_table['AvgPerTxn'].apply(lambda x: f"${x:,.2f}")
    emp_table['Unit'] = emp_table['Unit'].apply(lambda x: f"{x:,}")
    emp_table['Transaksi'] = emp_table['Transaksi'].apply(lambda x: f"{x:,}")
    
    cols_order = ['Peringkat', 'EmployeeName', 'EmployeeGender', 'Revenue', 'Transaksi', 'Unit', 'AvgPerTxn']
    st.dataframe(emp_table[cols_order], use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# TAB 5: DISCOUNT & ELASTICITY
# ------------------------------------------------------------------------------
with tab5:
    st.subheader("🏷️ Analisis Pengaruh Diskon terhadap Pendapatan dan Volume")
    
    disc_summary = df.groupby('Discount').agg(
        Revenue=('TotalPrice', 'sum'),
        Unit=('Quantity', 'sum'),
        Transaksi=('FactID', 'count'),
        AvgTxnVal=('TotalPrice', 'mean')
    ).reset_index()
    disc_summary['TingkatDiskon'] = disc_summary['Discount'].apply(lambda x: f"{x*100:.0f}%")
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        fig_disc_rev = px.pie(
            disc_summary,
            values='Revenue',
            names='TingkatDiskon',
            title="Proporsi Revenue Berdasarkan Besaran Diskon",
            hole=0.4,
            color_discrete_sequence=['#14B8A6', '#F59E0B', '#EF4444']
        )
        style_chart(fig_disc_rev, height=380)
        st.plotly_chart(fig_disc_rev, use_container_width=True)
        
    with col_d2:
        fig_disc_bar = px.bar(
            disc_summary,
            x='TingkatDiskon',
            y='AvgTxnVal',
            title="Rata-rata Nilai Transaksi (AOV) per Tingkat Diskon",
            labels={'TingkatDiskon': 'Tingkat Diskon', 'AvgTxnVal': 'Rata-rata Belanja ($)'},
            color='AvgTxnVal',
            color_continuous_scale='teal',
            text=disc_summary['AvgTxnVal'].apply(lambda x: f"${x:,.2f}")
        )
        style_chart(fig_disc_bar, height=380)
        fig_disc_bar.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_disc_bar, use_container_width=True)

    st.markdown("""
    <div class="info-callout">
        💡 <b>Insight Bisnis Manajerial</b>: Transaksi tanpa diskon (0%) menyumbang lebih dari <b>82%</b> total revenue toko. 
        Meskipun diskon 10% dan 20% diberikan, kuantitas unit per transaksi tidak meningkat signifikan, 
        sehingga promosi diskon sebaiknya difokuskan pada produk yang memiliki elastisitas tinggi (kategori perishable / vitality days rendah).
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 6: STAR SCHEMA & DATA EXPLORER
# ------------------------------------------------------------------------------
with tab6:
    st.subheader("🗄️ Arsitektur Star Schema & Eksplorasi Data Terintegrasi")
    
    col_arch1, col_arch2 = st.columns([1, 1])
    
    with col_arch1:
        st.markdown("""
        #### 📌 Desain Skema Bintang (Star Schema Architecture)
        * **1 Fact Table**: `FactSales` (200.000 records transaksi penjualan bersih)
        * **6 Dimension Tables**:
          * `DimWaktu` (130 hari kalender unik)
          * `DimProduct` (452 katalog produk denormalisasi)
          * `DimCategory` (11 kategori barang grocery)
          * `DimCustomer` (98.759 data pelanggan terintegrasi)
          * `DimCity` (96 kota terintegrasi negara)
          * `DimEmployee` (23 karyawan kasir supermarket)
        * **Measures Kuantitatif**: `Quantity`, `Discount`, `TotalPrice`
        * **Degenerate Dimension**: `TransactionNumber` (ID Struk Kasir)
        """)
        
    with col_arch2:
        st.markdown("""
        #### 🔍 Berkas Desain Skema:
        * Berkas visual grafik beresolusi tinggi tersedia di: `Star Schema/star_schema_diagram.png`.
        * Berkas mentah yang dapat diedit langsung tersedia di: `Star Schema/star_schema_grocery.drawio`.
        * Penampil web interaktif dark mode tersedia di: `Star Schema/schema_designer.html`.
        """)

    st.divider()
    st.markdown("#### 📋 Fact Table Browser (Real-Time Filter)")
    
    sample_cols = ['FactID', 'TransactionNumber', 'Tanggal', 'ProductName', 'CategoryName', 'CustomerName', 'CityName', 'EmployeeName', 'Quantity', 'Discount', 'TotalPrice']
    st.dataframe(df[sample_cols].head(100), use_container_width=True, hide_index=True)
    
    csv_data = df[sample_cols].head(5000).to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Unduh Data Terfilter (CSV)",
        data=csv_data,
        file_name="grocery_dwh_filtered_export.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748B; font-size: 13px;'>"
    "Grocery Sales Data Warehouse Analytics Dashboard • Dark Theme Edition • Dibangun dengan Streamlit & Star Schema MySQL • 2026"
    "</div>",
    unsafe_allow_html=True
)
