import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Monitoring Deposito dan Bunga", layout="wide")
st.title("Dashboard Monitoring Deposito dan Bunga")

CSV_URL = "https://docs.google.com/spreadsheets/d/1eoIkgdM2IH513xAx9A_IcumdH23Tw29fvc-KzSrkuGk/export?format=csv"

@st.cache_data(show_spinner=False)
def load_data(url: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df['KATEGORI'] = df['KATEGORI'].astype(str).str.strip().str.upper()
        df['BANK'] = df['BANK'].astype(str).str.strip()
        df['BULAN'] = df['BULAN'].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Gagal memuat data dari Google Sheets: {e}")
        return pd.DataFrame()

df_all = load_data(CSV_URL)

if df_all.empty or not set(['KATEGORI', 'BANK', 'BULAN', 'AMOUNT']).issubset(df_all.columns):
    st.warning("Data tidak memiliki struktur kolom yang lengkap.")
    st.stop()

# Siapkan pilihan filter
kategori_list = ['DEPOSITO', 'BUNGA']
for kategori in kategori_list:
    df_kat = df_all[df_all['KATEGORI'] == kategori]
    st.subheader(f"Tabel {kategori.title()}")

    # Ambil filter
    col1, col2 = st.columns(2)
    with col1:
        bank_filter = st.selectbox(f"Pilih Bank ({kategori})", ["Semua"] + sorted(df_kat['BANK'].dropna().unique().tolist()), key=f"bank_{kategori}")
    with col2:
        bulan_filter = st.selectbox(f"Pilih Bulan ({kategori})", ["Semua"] + sorted(df_kat['BULAN'].dropna().unique().tolist()), key=f"bulan_{kategori}")

    if bank_filter != "Semua":
        df_kat = df_kat[df_kat['BANK'] == bank_filter]
    if bulan_filter != "Semua":
        df_kat = df_kat[df_kat['BULAN'] == bulan_filter]

    # Tampilkan tabel
    df_display = df_kat[['BULAN', 'BANK', 'AMOUNT']].reset_index(drop=True)
    st.dataframe(df_display)

st.caption("*Dashboard ini menampilkan data berdasarkan kolom vertikal 'BULAN', 'BANK', dan 'AMOUNT' sesuai kategori.*")
