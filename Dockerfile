#این فایل ایمیج اپلیکیشن FastAPI رو می‌سازه:

# استفاده از پایتون سبک
FROM python:3.11-slim

# ست کردن working directory
WORKDIR /app

# کپی کردن فایل‌های مورد نیاز
COPY requirements.txt .

# نصب پکیج‌ها
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن کل پروژه داخل کانتینر
COPY . .

# اکسپوز کردن پورت uvicorn
EXPOSE 8000

# فرمان اجرای کانتینر با uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
