import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Deposito Bulanan", layout="wide")
st.title("Dashboard Monitoring Deposito dan Bunga")

CSV_URL = "https://docs.google.com/spreadsheets/d/1eoIkgdM2IH513xAx9A_IcumdH23Tw29fvc-KzSrkuGk/export?format=csv"

@st.cache_data(show_spinner=False)
def load_data(url: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Gagal memuat data dari Google Sheets: {e}")
        return pd.DataFrame()

df_all = load_data(CSV_URL)

if df_all.empty:
    st.warning("Data kosong atau tidak berhasil dimuat.")
    st.stop()

# Pisahkan berdasarkan tabel: deteksi berdasarkan baris 'KATEGORI' atau lainnya
if 'KATEGORI' in df_all.columns:
    df_all = df_all.ffill()  # pastikan kategori terisi
    df_depo = df_all[df_all['KATEGORI'].str.lower() == 'deposito']
    df_bunga = df_all[df_all['KATEGORI'].str.lower().str.contains('bunga')]
else:
    st.error("Kolom 'KATEGORI' tidak ditemukan untuk memisahkan tabel. Harap tambahkan kolom penanda kategori pada Google Sheets.")
    st.stop()

# Fungsi bantu untuk filter dan tampilkan tabel
def tampilkan_tabel(df, nama):
    st.subheader(f"Tabel {nama}")

    # Deteksi kolom
    month_keywords = ["jan", "feb", "mar", "apr", "mei", "jun", "jul", "agu", "aug", "sep", "okt", "oct", "nov", "des", "dec"]
    month_columns = [col for col in df.columns if any(k in col.lower() for k in month_keywords)]
    base_candidates = ["bank", "jatuh tempo", "bilyet", "amount", "rate", "interest"]
    base_columns = [col for col in df.columns if any(k in col.lower() for k in base_candidates)]
    bank_column = next((col for col in df.columns if 'bank' in col.lower()), None)

    col1, col2 = st.columns(2)
    with col1:
        selected_bank = st.selectbox(f"Pilih Bank ({nama})", ["Semua"] + sorted(df[bank_column].dropna().unique().tolist()) if bank_column else ["Semua"])
    with col2:
        selected_month = st.selectbox(f"Pilih Bulan ({nama})", ["Semua"] + month_columns)

    # Filter
    if selected_bank != "Semua" and bank_column:
        df = df[df[bank_column] == selected_bank]
    if selected_month != "Semua" and selected_month in df.columns:
        tampilkan = base_columns + [selected_month] if selected_month else base_columns
    else:
        tampilkan = base_columns + month_columns

    if not df.empty:
        st.dataframe(df[tampilkan].reset_index(drop=True))
    else:
        st.info(f"Tidak ada data yang sesuai di tabel {nama}.")

# Tampilkan kedua tabel
tampilkan_tabel(df_depo, "Deposito")
tampilkan_tabel(df_bunga, "Bunga Deposito")

st.caption("*Data ditampilkan berdasarkan dua kategori: Deposito dan Bunga, dengan filter bank dan bulan secara terpisah.*")
