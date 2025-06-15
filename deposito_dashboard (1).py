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

# Bagi data menjadi dua berdasarkan nilai di kolom 'KATEGORI'
if 'KATEGORI' in df_all.columns:
    df_all = df_all.ffill()
    df_depo = df_all[df_all['KATEGORI'].str.lower() == 'deposito']
    df_bunga = df_all[df_all['KATEGORI'].str.lower().str.contains('bunga')]
else:
    st.error("Kolom 'KATEGORI' tidak ditemukan. Tambahkan kolom ini untuk memisahkan antara deposito dan bunga.")
    st.stop()

# Fungsi bantu
month_keywords = ["jan", "feb", "mar", "apr", "mei", "jun", "jul", "agu", "aug", "sep", "okt", "oct", "nov", "des", "dec"]

def detect_month_columns(columns):
    return [col for col in columns if any(k in col.lower() for k in month_keywords)]

def display_table(df, title, value_column_label):
    st.subheader(f"Tabel {title}")

    # Identifikasi kolom bulan dan bank
    month_columns = detect_month_columns(df.columns)
    bank_column = next((col for col in df.columns if 'bank' in col.lower()), None)

    if not bank_column:
        st.warning("Kolom 'Bank' tidak ditemukan pada tabel " + title)
        return

    selected_bank = st.selectbox(f"Pilih Bank ({title})", ["Semua"] + sorted(df[bank_column].dropna().unique().tolist()))
    selected_month = st.selectbox(f"Pilih Bulan ({title})", ["Semua"] + month_columns)

    # Filter bank
    if selected_bank != "Semua":
        df = df[df[bank_column] == selected_bank]

    # Persiapkan data tampil
    tampil_col = [bank_column]
    if selected_month != "Semua" and selected_month in df.columns:
        tampil_col.append(selected_month)
    else:
        tampil_col += month_columns

    df_display = df[tampil_col].rename(columns={selected_month: value_column_label} if selected_month != "Semua" else {})

    st.dataframe(df_display.reset_index(drop=True))

# Tampilkan tabel Deposito dan Bunga
with st.expander("📌 Tabel Deposito", expanded=True):
    display_table(df_depo, "Deposito", "Nominal")

with st.expander("💰 Tabel Bunga Deposito", expanded=True):
    display_table(df_bunga, "Bunga Deposito", "Amount")

st.caption("*Filter berdasarkan Bank dan Bulan (horizontal) berlaku untuk masing-masing tabel.*")
