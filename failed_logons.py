import win32evtlog
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

# -----------------------------
# تنظیمات پایه
# -----------------------------
SERVER = "localhost"
EVENT_LOG = "Security"
EVENT_ID = 4625  # Failed Logon
OUTPUT_FILE = "failed_logons.csv"

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# -----------------------------
# خواندن لاگ‌های لاگین ناموفق
# -----------------------------
def read_failed_logons(server=SERVER, event_id=EVENT_ID):
    handle = win32evtlog.OpenEventLog(server, EVENT_LOG)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events = []

    while True:
        records = win32evtlog.ReadEventLog(handle, flags, 0)
        if not records:
            break

        for event in records:
            if event.EventID == event_id:
                events.append({
                    "Time": event.TimeGenerated.Format(),
                    "Source": event.SourceName,
                    "Details": " | ".join(event.StringInserts) if event.StringInserts else "N/A"
                })

    win32evtlog.CloseEventLog(handle)
    return events

# -----------------------------
# ذخیره در فایل CSV
# -----------------------------
def save_to_csv(events, filename=OUTPUT_FILE):
    df = pd.DataFrame(events)
    df.to_csv(filename, index=False, encoding="utf-8")
    return os.path.abspath(filename)

# -----------------------------
# ارسال ایمیل
# -----------------------------
def send_email(file_path, events_found: bool):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = "Windows Failed Logon Report"

    if events_found:
        body = "لطفاً گزارش لاگین‌های ناموفق ویندوز را در فایل پیوست مشاهده کنید."
    else:
        body = "هیچ لاگین ناموفقی پیدا نشد. سیستم سالم است."

    msg.attach(MIMEText(body, "plain"))

    # پیوست فایل حتی اگر خالی باشد
    with open(file_path, "rb") as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
        msg.attach(part)

    # ارسال ایمیل
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

# -----------------------------
# اجرای اصلی
# -----------------------------
if __name__ == "__main__":
    print("[*] در حال خواندن لاگ‌های ناموفق...")
    failed_logons = read_failed_logons()

    if not failed_logons:
        print("[+] لاگ ناموفق یافت نشد. همه چیز درست است.")
    else:
        print(f"[+] تعداد {len(failed_logons)} لاگ ناموفق یافت شد.")

    file_path = save_to_csv(failed_logons)
    print(f"[+] گزارش در {file_path} ذخیره شد.")

    print("[*] در حال ارسال ایمیل...")
    send_email(file_path, events_found=bool(failed_logons))
    print("[+] ایمیل با موفقیت ارسال شد.")
