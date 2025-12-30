import pandas as pd
from datetime import datetime
import os

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "transactions.csv")

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

def delete_transaction_by_id(trans_id):
    df = load_data()
    df = df[df["id"] != trans_id]
    save_data(df)
