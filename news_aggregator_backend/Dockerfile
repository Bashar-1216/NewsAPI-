# استخدم صورة Python 3.11
FROM python:3.11-slim

# إعداد مجلد العمل
WORKDIR /app

# نسخ ملفات المشروع
COPY . /app

# تحديث pip وتثبيت wheel و setuptools
RUN pip install --upgrade pip setuptools wheel

# تثبيت نسخ متوافقة من transformers و tokenizers لتجنب Rust
RUN pip install \
    tokenizers==0.13.3 \
    transformers==4.29.2

# تثبيت باقي المتطلبات من requirements.txt بدون tokenizers و transformers
RUN pip install --no-deps -r requirements.txt

# فتح البورت الذي يستخدمه Railway
EXPOSE 8080

# أمر التشغيل الافتراضي باستخدام Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "src.main:app"]
