import streamlit as st
import pandas as pd
import altair as alt
import re

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Deposito Bulanan", layout="wide")

# Judul Aplikasi
st.title("Dashboard Monitoring Deposito Bulanan")

# URL Google Sheets publik (format CSV) 
CSV_URL = "https://docs.google.com/spreadsheets/d/1Ouct7adiZK51oI2DVtU56kMDqE-exQ3ljFtaWnGuXkc/export?format=csv"

@st.cache_data
def load_data(url: str) -> pd.DataFrame:
    return pd.read_csv(url)

df = load_data(CSV_URL)

# Validasi kolom
expected_cols = {"Bulan", "Bank", "Saldo"}
if not expected_cols.issubset(df.columns):
    st.error("Kolom data tidak sesuai. Pastikan terdapat kolom 'Bulan', 'Bank', dan 'Saldo'.")
    st.stop()

ALL = "Semua"

def parse_month(month_str: str):
    try:
        return pd.to_datetime(month_str, dayfirst=False)
    except Exception:
        mapping = {
            "Januari": 1, "Februari": 2, "Maret": 3, "April": 4, "Mei": 5, "Juni": 6,
            "Juli": 7, "Agustus": 8, "September": 9, "Oktober": 10, "November": 11, "Desember": 12,
            "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Mei": 5, "Jun": 6,
            "Jul": 7, "Aug": 8, "Agu": 8, "Sep": 9, "Oct": 10, "Okt": 10, "Nov": 11, "Dec": 12
        }
        match = re.search(r"(\d{4})", month_str)
        year = int(match.group(1)) if match else None
        month_num = None
        for name, num in mapping.items():
            if name in month_str:
                month_num = num
                break
        if year and month_num:
            return pd.Timestamp(year, month_num, 1)
        else:
            return None

unique_months = df["Bulan"].unique()
unique_banks = df["Bank"].unique()
months_sorted = sorted(unique_months, key=lambda x: parse_month(x) or x)
bank_options = sorted(unique_banks)
month_options = [ALL] + months_sorted
bank_options = [ALL] + bank_options

# Sidebar
st.sidebar.header("Filter")
selected_month = st.sidebar.selectbox("Filter Bulan", month_options)
selected_bank = st.sidebar.selectbox("Filter Bank", bank_options)

# Filter data
df_filtered = df.copy()
if selected_month != ALL:
    df_filtered = df_filtered[df_filtered["Bulan"] == selected_month]
if selected_bank != ALL:
    df_filtered = df_filtered[df_filtered["Bank"] == selected_bank]

summary_df = df_filtered.groupby("Bulan")["Saldo"].sum().reset_index()
summary_df["Month_dt"] = summary_df["Bulan"].apply(parse_month)
summary_df = summary_df.dropna(subset=["Month_dt"]).sort_values("Month_dt")
summary_df.rename(columns={"Saldo": "Total Saldo"}, inplace=True)

# Format Total Saldo sebagai mata uang
summary_df["Total Saldo"] = summary_df["Total Saldo"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))

bar_df = df_filtered.groupby("Bank")["Saldo"].sum().reset_index().rename(columns={"Saldo": "Total Saldo"})
bar_df.sort_values("Total Saldo", ascending=False, inplace=True)

line_chart = alt.Chart(summary_df).mark_line(point=True).encode(
    x=alt.X("Month_dt:T", title="Bulan"),
    y=alt.Y("Total Saldo:Q", title="Total Saldo"),
    tooltip=[alt.Tooltip("Bulan:N"), alt.Tooltip("Total Saldo:Q")]
).properties(height=400)

bar_chart = alt.Chart(bar_df).mark_bar().encode(
    x=alt.X("Bank:N", sort=None, title="Bank"),
    y=alt.Y("Total Saldo:Q", title="Total Saldo"),
    tooltip=[alt.Tooltip("Bank:N"), alt.Tooltip("Total Saldo:Q")]
).properties(height=400)

# Output
st.subheader("Ringkasan Deposito per Bulan")
st.dataframe(summary_df[["Bulan", "Total Saldo"]])

st.subheader("Distribusi Saldo per Bank")
if selected_bank != ALL:
    st.caption(f"*Hanya menampilkan Bank **{selected_bank}** pada bulan terfilter.*")
st.altair_chart(bar_chart, use_container_width=True)

st.subheader("Tren Saldo Bulanan")
if selected_month != ALL:
    st.caption(f"*Hanya menampilkan data bulan **{selected_month}** untuk bank terfilter.*")
st.altair_chart(line_chart, use_container_width=True)
