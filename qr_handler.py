import qrcode
import cv2
import numpy as np
import os

QR_DIR = "qr"

def generate_qr_category(kategori):
    filename = os.path.join(QR_DIR, f"cat_{kategori}.png")
    img = qrcode.make(f"CAT:{kategori}")
    img.save(filename)
    return filename

def scan_qr(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    return data
