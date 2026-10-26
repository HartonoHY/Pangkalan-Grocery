# 🛒 Grocery Sales Data Warehouse - Cloud Analytics Dashboard

Interactive modern Dark-Mode Data Warehouse Dashboard built with **Streamlit**, **Plotly**, and **Star Schema** architecture (200,000 facts, 6 dimensions).

## 🚀 Live Demo & Deployment
Aplikasi ini sudah dioptimasi untuk deployment 24/7 di **Streamlit Community Cloud** atau **Hugging Face Spaces**.

### Cara Deploy ke Streamlit Cloud:
1. Fork atau push repositori ini ke GitHub.
2. Buka [share.streamlit.io](https://share.streamlit.io).
3. Pilih repository ini, tentukan main file: `app.py`.
4. Klik **Deploy**!

## 📊 Fitur Utama Dashboard
1. **Executive Overview (Ringkasan Eksekutif):** 4 Metrik Kartu KPI Utama ($127.94M Revenue, 200k Transaksi, 99.8k Qty Terjual, Avg Discount 20.03%), Visual Tren Pendapatan Bulanan & Distribusi Kelas Harga.
2. **Produk & Kategori:** Pareto Top 10 Produk, Kategori Terlaris, Analisis Vitality Days (Kedaluwarsa Bahan Makanan).
3. **Pelanggan & Geografi:** Top 10 Kota Kontributor Revenue Terbesar, Kontribusi Pelanggan VIP, Distribusi Global.
4. **Karyawan Kasir:** Ranking Penjualan Kasir, Breakdown Proporsi Gender Karyawan.
5. **Diskon & Elastisitas Harga:** Scatter Plot Hubungan Tingkat Diskon vs Volume Pembelian & Tren Efektivitas Promosi.
6. **Star Schema & Data Explorer:** Visual Relasi Star Schema DWH & Tabel Data Interaktif 200.000 Transaksi lengkap dengan fitur Filter Dinamis dan tombol Export ke CSV.

## 🛠️ Arsitektur Data
- **Engine Data:** High-Speed Apache Parquet (`data/grocery_sales_dwh.parquet`) dengan kompresi Snappy untuk performa rendering seketika (< 0.5 detik).
- **Fallback:** Live MySQL Engine via SQLAlchemy & Cleaned CSV.
