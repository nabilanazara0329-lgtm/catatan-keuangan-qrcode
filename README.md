# Aplikasi Catatan Keuangan dengan QR Code

## Deskripsi
Aplikasi berbasis Streamlit untuk mencatat pemasukan dan pengeluaran
harian dengan bantuan QR Code sebagai input kategori transaksi.

## Fitur
- Menambah transaksi pemasukan dan pengeluaran
- Scan QR Code untuk memilih kategori
- Generate QR Code kategori
- Menampilkan grafik pengeluaran per kategori
- Backup data transaksi ke file ZIP

## Cara Menjalankan Aplikasi
1. Install library yang dibutuhkan:
   pip install -r requirements.txt
2. Jalankan aplikasi:
   streamlit run app.py

## Struktur Folder
- app.py : file utama aplikasi
- data/ : menyimpan data transaksi (CSV)
- qr/ : menyimpan QR Code kategori
- backup/ : menyimpan file cadangan data
- requirements.txt : daftar library Python

## Author
- Nabila Nazara Suci
- Dea Fani Mutmainah
- Emmi Andhary
- Selfi Fitria Anggraini
