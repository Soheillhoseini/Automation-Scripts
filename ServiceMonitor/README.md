Service Monitor

توضیح پروژه:
این اسکریپت Python برای اتوماسیون Help Desk طراحی شده است و وضعیت سرویس‌ها و سرورهای مهم را بررسی می‌کند.  
اگر هر سرویسی Down باشد، هشدار ایمیل با فایل CSV شامل جزئیات سرویس‌ها ارسال می‌شود.

## ویژگی‌ها
- بررسی سرویس‌های مهم TCP (DNS, HTTP, HTTPS, RDP, SQL, SMTP و غیره)
- تولید CSV خروجی با زمان، نام سرویس، هاست، پورت و وضعیت
- ارسال ایمیل هشدار فقط در صورت Down بودن سرویس‌ها


## پیش‌نیازها
- Python 3.x نصب شده
- حساب Gmail برای ارسال ایمیل
- اجرای اسکریپت به عنوان Administrator

## نصب کتابخانه‌ها
کتابخانه‌های استاندارد Python کافی هستند، برای CSV ساده نیازی به نصب اضافه نیست.

## نحوه استفاده
1. ایمیل و App Password خود را در فایل اسکریپت تنظیم کنید:

```python
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"
