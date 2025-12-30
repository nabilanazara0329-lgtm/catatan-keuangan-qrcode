import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime
import os
import matplotlib.pyplot as plt
import base64
import zipfile
import qrcode

KATEGORI_LIST = ["Makan", "Transport", "Belanja", "Hiburan", "Lainnya"]


# ----- Folder & File Setup -----
DATA_DIR = "data"
QR_DIR = "qr"
BACKUP_DIR = "backup"
DATA_FILE = os.path.join(DATA_DIR, "transactions.csv")


def init_folders():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(QR_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    

# ----- Data Handling -----
def load_data(file_path=DATA_FILE):
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["id", "tanggal", "kategori", "nominal", "tipe", "catatan"])
        df.to_csv(file_path, index=False)
        return df
    return pd.read_csv(file_path, dtype={"id": str})


def save_data(df, file_path=DATA_FILE):
    df.to_csv(file_path, index=False)


def add_transaction(kategori, nominal, tipe, catatan):
    df = load_data()
    new_id = f"T{int(datetime.now().timestamp() * 1000)}"
    row = {
        "id": new_id,
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "kategori": kategori,
        "nominal": float(nominal),
        "tipe": tipe,
        "catatan": catatan
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    save_data(df)
    return new_id


def read_transactions():
    return load_data()

def delete_transaction_by_id(trans_id):
    df = load_data()
    df = df[df["id"] != trans_id]
    save_data(df)


# ----- QR Functions -----
def generate_qr_category(kategori):
    filename = os.path.join(QR_DIR, f"cat_{kategori.replace(' ', '_')}.png")
    payload = f"CAT:{kategori}"
    img = qrcode.make(payload)
    img.save(filename)
    return filename


def scan_qr_opencv(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        return [data]
    return []


# ----- Statistik, Grafik, Backup -----
def get_summary_stats(df):
    pemasukan = df[df['tipe'] == "pemasukan"]["nominal"].sum()
    pengeluaran = df[df['tipe'] == "pengeluaran"]["nominal"].sum()
    saldo = pemasukan - pengeluaran
    return {
        "pemasukan": pemasukan,
        "pengeluaran": pengeluaran,
        "saldo": saldo
    }


def create_category_pie(df):
    if df.empty:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No Data", ha='center')
        return fig

    grp = df.groupby("kategori")["nominal"].sum()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(grp.values, labels=grp.index, autopct='%1.1f%%')
    return fig


def backup_csv():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zipname = os.path.join(BACKUP_DIR, f"backup_{timestamp}.zip")

    with zipfile.ZipFile(zipname, 'w') as zf:
        for folder, _, files in os.walk(DATA_DIR):
            for f in files:
                zf.write(os.path.join(folder, f))

    return zipname


def get_download_link(file_path, label="Download"):
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f'<a href="data:file/zip;base64,{b64}" download="{os.path.basename(file_path)}">{label}</a>'


# ===== STREAMLIT UI =====
def main():
    init_folders()
    st.markdown("""
    <style>
    /* ===== FONT & BACKGROUND ===== */
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
    }

    /* ===== JUDUL ===== */
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }

    /* ===== CARD ===== */
    .card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    /* ===== TABEL DATA ===== */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ===== METRIC ===== */
    div[data-testid="metric-container"] {
        background: #ffffff;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617, #312e81);
        color: white;
    }

    section[data-testid="stSidebar"] * {
        color: black;
    }

    /* ===== BUTTON ===== */
    .stButton>button {
        border-radius: 10px;
        background-color: #2ecc71;
        color: white;
        font-weight: bold;
        padding: 8px 18px;
        border: none;
    }

    .stButton>button:hover {
        background-color: #27ae60;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


    st.markdown('<div class="title">📒 Catatan Keuangan Pribadi + QR Scanner</div>', unsafe_allow_html=True)

    menu = st.sidebar.selectbox("Menu", ["Dashboard", "Tambah Transaksi", "Scan QR", "Generate QR", "Data"])

    # Dashboard
    if menu == "Dashboard":
        df = read_transactions()
        stats = get_summary_stats(df)

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Pemasukan", f"Rp {stats['pemasukan']:,}")
        col2.metric("💸 Pengeluaran", f"Rp {stats['pengeluaran']:,}")
        col3.metric("📊 Saldo", f"Rp {stats['saldo']:,}")

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📈 Grafik Kategori")
        st.pyplot(create_category_pie(df))
        st.markdown("</div>", unsafe_allow_html=True)

    # Tambah Transaksi
    elif menu == "Tambah Transaksi":
        st.subheader(" Tambah Transaksi")
        
        kategori = st.selectbox("Pilih Kategori", KATEGORI_LIST)
        
        nominal = st.number_input("Nominal", min_value=0.0)
        tipe = st.selectbox("Tipe", ["pengeluaran", "pemasukan"])
        catatan = st.text_area("Catatan")
        
        if st.button("Simpan"):
            add_transaction(kategori, nominal, tipe, catatan)
            st.success("Transaksi tersimpan!")

    # Scan QR
    elif menu == "Scan QR":
        st.subheader("📷 Scan QR Code")
        img_file = st.camera_input("Arahkan QR ke kamera lalu klik Capture")

        if img_file:
            data = scan_qr_opencv(img_file.read())

            if data:
                qr = data[0]
                st.success(f"Hasil scan: **{qr}**")

                if qr.startswith("CAT:"):
                    kategori = qr.replace("CAT:", "")
                    st.info(f"Kategori terdeteksi: {kategori}")

                    nominal = st.number_input("Nominal", min_value=0.0)
                    tipe = st.selectbox("Tipe", ["pengeluaran", "pemasukan"])
                    catatan = st.text_area("Catatan")

                    if st.button("Simpan Transaksi"):
                        add_transaction(kategori, nominal, tipe, catatan)
                        st.success("Transaksi dari QR berhasil disimpan!")
                else:
                    st.error("QR tidak valid (format harus: CAT:<kategori>)")
            else:
                st.error("QR tidak terbaca.")

    # Generate QR
    elif menu == "Generate QR":
        st.subheader("🔧 Buat QR untuk Kategori")

        kategori = st.selectbox("Pilih Kategori", KATEGORI_LIST)

        if st.button("Generate"):
            filename = generate_qr_category(kategori)
            st.image(filename, width=200)
            st.success("QR kategori berhasil dibuat!")
        
    # Data
    elif menu == "Data":
        st.subheader("📄 Data Transaksi")

        df = read_transactions()

        if df.empty:
            st.info("Belum ada data transaksi.")
        else:
            df_tampil = df.copy()

            # Kolom pengeluaran & pemasukan
            df_tampil["pengeluaran"] = df_tampil.apply(
                lambda x: x["nominal"] if x["tipe"] == "pengeluaran" else "",
                axis=1
            )

            df_tampil["pemasukan"] = df_tampil.apply(
                lambda x: x["nominal"] if x["tipe"] == "pemasukan" else "",
                axis=1
            )

            # Urutan kolom
            df_tampil = df_tampil[
                ["id", "tanggal", "kategori", "nominal", "pengeluaran", "pemasukan", "catatan"]
            ]

            st.dataframe(df_tampil, use_container_width=True)
            
            # ===== HAPUS DATA =====
            st.markdown("### 🗑️ Hapus Transaksi")

            id_list = df["id"].tolist()
            selected_id = st.selectbox("Pilih ID Transaksi", id_list)

            if st.button("Hapus Data"):
                delete_transaction_by_id(selected_id)
                st.success("Data berhasil dihapus!")
                st.rerun()

            # Ringkasan
            col1, col2 = st.columns(2)
            col1.error(f"Total Pengeluaran: Rp {df[df['tipe']=='pengeluaran']['nominal'].sum():,}")
            col2.success(f"Total Pemasukan: Rp {df[df['tipe']=='pemasukan']['nominal'].sum():,}")

        st.divider()

        if st.button("Backup CSV"):
            z = backup_csv()
            st.success("Backup berhasil dibuat.")
            st.markdown(get_download_link(z), unsafe_allow_html=True)
            

if __name__ == "__main__":
    main()