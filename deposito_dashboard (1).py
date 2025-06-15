import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Monitoring Deposito dan Bunga", layout="wide")
st.title("📊 Dashboard Monitoring Deposito dan Bunga")

# URL Google Sheet sebagai CSV publik
CSV_URL = "https://docs.google.com/spreadsheets/d/1eoIkgdM2IH513xAx9A_IcumdH23Tw29fvc-KzSrkuGk/export?format=csv"

# Fungsi memuat dan membersihkan data
@st.cache_data(show_spinner=False)
def load_data(url: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df["KATEGORI"] = df["KATEGORI"].astype(str).str.strip().str.upper()
        df["BANK"] = df["BANK"].astype(str).str.strip().str.upper()
        df["BULAN"] = df["BULAN"].astype(str).str.strip().str.upper()
        df["AMOUNT"] = (
            df["AMOUNT"]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        df["AMOUNT"] = pd.to_numeric(df["AMOUNT"], errors="coerce")
        return df.dropna(subset=["AMOUNT"])
    except Exception as e:
        st.error(f"Gagal memuat data dari Google Sheets: {e}")
        return pd.DataFrame()

# Ambil data
df_all = load_data(CSV_URL)

# Validasi struktur minimal
required_cols = {"KATEGORI", "BANK", "BULAN", "AMOUNT"}
if df_all.empty or not required_cols.issubset(set(df_all.columns)):
    st.warning("Struktur data tidak lengkap.")
    st.stop()

# Tampilkan tabel berdasarkan KATEGORI
for kategori in ["DEPOSITO", "BUNGA"]:
    st.subheader(f"📌 Tabel {kategori.title()}")
    df_kat = df_all[df_all["KATEGORI"] == kategori]

    if df_kat.empty:
        st.info(f"Tidak ada data untuk kategori {kategori}.")
        continue

    # Ambil opsi filter
    bank_options = sorted(df_kat["BANK"].unique().tolist())
    bulan_options = sorted(df_kat["BULAN"].unique().tolist())

    col1, col2 = st.columns(2)
    with col1:
        selected_bank = st.selectbox(f"Pilih Bank ({kategori})", ["Semua"] + bank_options, key=f"bank_{kategori}")
    with col2:
        selected_bulan = st.selectbox(f"Pilih Bulan ({kategori})", ["Semua"] + bulan_options, key=f"bulan_{kategori}")

    # Terapkan filter hanya jika bukan 'Semua'
    if selected_bank != "Semua":
        df_kat = df_kat[df_kat["BANK"] == selected_bank]
    if selected_bulan != "Semua":
        df_kat = df_kat[df_kat["BULAN"] == selected_bulan]

    # Tampilkan hasil
    if df_kat.empty:
        st.info("Tidak ada data yang sesuai dengan filter.")
    else:
        df_show = df_kat[["BULAN", "BANK", "AMOUNT"]].copy()
        df_show["AMOUNT"] = df_show["AMOUNT"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
        st.dataframe(df_show.reset_index(drop=True))

# Footer
st.caption("*Data ditarik dari satu tabel dan ditampilkan berdasarkan nilai kolom 'KATEGORI'. Format nominal dalam Rupiah.*")
