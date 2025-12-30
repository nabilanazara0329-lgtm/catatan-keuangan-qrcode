import os
import zipfile
from datetime import datetime
import base64

DATA_DIR = "data"
BACKUP_DIR = "backup"

def init_folders():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(QR_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)

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
