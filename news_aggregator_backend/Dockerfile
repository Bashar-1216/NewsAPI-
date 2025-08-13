# استخدم صورة Python 3.11 خفيفة
FROM python:3.11-slim

# إعداد مجلد العمل
WORKDIR /app

# نسخ ملفات المشروع
COPY . /app

# تحديث pip وتثبيت wheel و setuptools
RUN pip install --upgrade pip setuptools wheel

# تثبيت الحزم الكبيرة أولًا لتجنب مشاكل Rust
# تثبيت الحزم الكبيرة أولًا لتجنب مشاكل Rust
RUN pip install \
    torch==2.2.0 \
    scikit-learn==1.3.2 \
    scipy==1.11.3 \
    transformers==4.29.2 \
    tokenizers==0.13.3


# تثبيت باقي الحزم من requirements.txt بدون إعادة تثبيت الحزم السابقة
RUN pip install --no-deps -r requirements.txt

# فتح البورت الذي يستخدمه Railway
EXPOSE 8080

CMD ["python", "src/main.py"]
