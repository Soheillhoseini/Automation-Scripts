import csv
import socket
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# -----------------------------
# تنظیمات سرویس‌ها
# -----------------------------
SERVICES = [
    {"name": "Google DNS", "host": "8.8.8.8", "port": 53},
    {"name": "Local Web Server", "host": "127.0.0.1", "port": 80},
    {"name": "Local HTTPS", "host": "127.0.0.1", "port": 443},
    {"name": "Remote Desktop", "host": "192.168.1.10", "port": 3389},
    {"name": "SQL Server", "host": "192.168.1.20", "port": 1433},
    {"name": "SMTP Mail", "host": "smtp.gmail.com", "port": 587},
]

OUTPUT_FILE = "service_status.csv"

# -----------------------------
# ایمیل
# -----------------------------
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# -----------------------------
# بررسی سرویس TCP
# -----------------------------
def check_service(host, port, timeout=3):
    """Check if a TCP service is reachable"""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

# -----------------------------
# ذخیره CSV
# -----------------------------
def save_to_csv(results, filename=OUTPUT_FILE):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "service", "host", "port", "status"])
        writer.writeheader()
        writer.writerows(results)
    return filename

# -----------------------------
# ارسال ایمیل هشدار
# -----------------------------
def send_email(results, filename):
    all_up = all(r["status"] == "UP" for r in results)
    subject = "Service Monitor Report" if all_up else "Service Monitor Alert"
    body = "تمام سرویس‌ها در دسترس هستند." if all_up else "برخی سرویس‌ها در دسترس نیستند. لطفاً فایل پیوست را بررسی کنید."

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, "plain"))

    # پیوست CSV
    with open(filename, "rb") as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

# -----------------------------
# اجرای اصلی
# -----------------------------
if __name__ == "__main__":
    results = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("[*] بررسی سرویس‌ها در حال انجام است...")
    for svc in SERVICES:
        status = "UP" if check_service(svc["host"], svc["port"]) else "DOWN"
        results.append({
            "timestamp": timestamp,
            "service": svc["name"],
            "host": svc["host"],
            "port": svc["port"],
            "status": status
        })
        print(f"{svc['name']} ({svc['host']}:{svc['port']}) => {status}")

    csv_file = save_to_csv(results)
    print(f"[+] گزارش ذخیره شد: {csv_file}")

    print("[*] ارسال ایمیل هشدار...")
    send_email(results, csv_file)
    print("[+] ایمیل ارسال شد.")
