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
        df['BANK'] = df['BANK'].astype(str).str.strip().str.upper()
        df['BULAN'] = df['BULAN'].astype(str).str.strip().str.upper()
        df['AMOUNT'] = df['AMOUNT'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        df['AMOUNT'] = pd.to_numeric(df['AMOUNT'], errors='coerce')
        return df.dropna(subset=['AMOUNT'])
    except Exception as e:
        st.error(f"Gagal memuat data dari Google Sheets: {e}")
        return pd.DataFrame()

df_all = load_data(CSV_URL)

if df_all.empty or not set(['KATEGORI', 'BANK', 'BULAN', 'AMOUNT']).issubset(df_all.columns):
    st.warning("Data tidak memiliki struktur kolom yang lengkap.")
    st.stop()

kategori_list = ['DEPOSITO', 'BUNGA']
for kategori in kategori_list:
    df_kat = df_all[df_all['KATEGORI'] == kategori]
    st.subheader(f"Tabel {kategori.title()}")

    bank_list = sorted(df_kat['BANK'].dropna().unique().tolist())
    bulan_list = sorted(df_kat['BULAN'].dropna().unique().tolist())

    col1, col2 = st.columns(2)
    with col1:
        selected_bank = st.selectbox(f"Pilih Bank ({kategori})", ["Semua"] + bank_list, key=f"bank_{kategori}")
    with col2:
        selected_bulan = st.selectbox(f"Pilih Bulan ({kategori})", ["Semua"] + bulan_list, key=f"bulan_{kategori}")

    if selected_bank != "Semua":
        df_kat = df_kat[df_kat['BANK'] == selected_bank]
    if selected_bulan != "Semua":
        df_kat = df_kat[df_kat['BULAN'] == selected_bulan]

    if not df_kat.empty:
        df_display = df_kat[['BULAN', 'BANK', 'AMOUNT']].copy()
        df_display['AMOUNT'] = df_display['AMOUNT'].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
        st.dataframe(df_display.reset_index(drop=True))
    else:
        st.info("Tidak ada data yang sesuai dengan filter.")

st.caption("*Data ditampilkan berdasarkan kolom 'KATEGORI', dengan filter berdasarkan 'BANK' dan 'BULAN'.*")
