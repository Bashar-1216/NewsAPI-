# استخدم صورة Python 3.11 خفيفة
FROM python:3.11-slim

# إعداد مجلد العمل
WORKDIR /app

# نسخ ملفات المشروع
COPY . /app

# تحديث pip و wheel و setuptools
RUN pip install --upgrade pip setuptools wheel

# تثبيت الأدوات اللازمة لتثبيت scipy و scikit-learn على slim image
RUN apt-get update && apt-get install -y build-essential gfortran libopenblas-dev liblapack-dev

# تثبيت المكتبات الثقيلة أولًا لتجنب مشاكل البناء
RUN pip install scipy scikit-learn torch

# تثبيت باقي المكتبات من requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# فتح البورت الذي يستخدمه التطبيق داخليًا
EXPOSE 8080

CMD ["python", "src/main.py"]
