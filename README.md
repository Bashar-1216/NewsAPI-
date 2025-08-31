

---

```markdown
# 📰 NewsAI - نظام ذكي لجمع وتحليل الأخبار

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-Frontend-61dafb?logo=react)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-Design-38bdf8?logo=tailwind-css)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

**NewsAI** هو نظام متكامل يجمع الأخبار من مصادر متعددة ويحللها باستخدام تقنيات الذكاء الاصطناعي ومعالجة اللغات الطبيعية **(NLP)**، ليقدم تجربة قراءة مخصصة وذكية.

---

## 🚀 المميزات الرئيسية

### 📡 **جمع الأخبار الذكي**
- تكامل مع **NewsAPI** و**Google News API**.
- دعم جمع الأخبار حسب التصنيفات أو الكلمات المفتاحية.

### 🤖 **تحليل وتصنيف المحتوى**
- تصنيف تلقائي للأخبار (تكنولوجيا، صحة، سياسة...).
- تلخيص المقالات الطويلة باستخدام خوارزميات **NLP**.
- كشف الأخبار الزائفة وتقييم مصداقية المصادر.

### 📊 **تحليلات متقدمة**
- تحليل المشاعر العامة (إيجابي / سلبي / محايد).
- لوحات إحصائية تفاعلية توضح اتجاهات الأخبار.

### 🎨 **تجربة مستخدم مخصصة**
- بحث متقدم وتصفية المحتوى حسب الفئة والمصدر.
- واجهة بسيطة وحديثة باستخدام **React + Tailwind**.
- دعم تعدد اللغات (قريبًا).

---

## 🛠️ التقنيات المستخدمة

### **الواجهة الخلفية (Backend)**
- **Python 3.11+**
- **Flask** لإدارة الخادم والـ APIs
- **SQLite** كقاعدة بيانات محلية
- مكتبات الذكاء الاصطناعي:
  - **NLTK** و **TextBlob** لتحليل النصوص
  - **Scikit-learn** لتصنيف النصوص

### **الواجهة الأمامية (Frontend)**
- **React.js** لإنشاء واجهة ديناميكية
- **Tailwind CSS** للتصميم
- **shadcn/ui** و **Lucide Icons** للأيقونات والمكونات الجاهزة

---

## 📂 هيكل المشروع

```

news\_aggregator\_backend/
├── src/
│   ├── models/          # نماذج قاعدة البيانات
│   ├── routes/          # المسارات وواجهات API
│   ├── services/        # الخدمات وتحليل النصوص
│   ├── static/          # الملفات الثابتة
│   └── main.py          # نقطة تشغيل التطبيق
└── requirements.txt     # المتطلبات

news-aggregator-frontend/
├── src/
│   ├── components/      # مكونات React
│   ├── assets/          # الصور والملفات
│   └── App.jsx          # المكون الرئيسي
└── package.json         # إعدادات المشروع

````

---

## ⚡ التشغيل المحلي

### **1. إعداد الواجهة الخلفية**
```bash
cd news_aggregator_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
````

يفتح على: [http://localhost:5000](http://localhost:5000)

---

### **2. إعداد الواجهة الأمامية**

```bash
cd news-aggregator-frontend
pnpm install
pnpm run dev --host
```

يفتح على: [http://localhost:5173](http://localhost:5173)

---

## 🔮 الميزات القادمة

* دعم تسجيل الدخول وحفظ الأخبار المفضلة.
* إشعارات فورية للأخبار العاجلة.
* تطبيق للهواتف الذكية (iOS و Android).
* تحسينات لتحليل النصوص بدقة أعلى.

---

## 📸 لقطات شاشة مقترحة

* **الصفحة الرئيسية**: عرض أهم الأخبار.
* **لوحة الإحصائيات**: اتجاهات وتحليلات.
* **نتائج تحليل المشاعر**: توزيع المشاعر حسب الأخبار.

---

## 🤝 المساهمة

نرحب بالمساهمات!

1. قم بعمل **Fork** للمستودع.
2. أنشئ فرعًا جديدًا:

   ```bash
   git checkout -b feature-name
   ```
3. أرسل **Pull Request** بعد الانتهاء.

---


---


---

```

هل تريد أن أضيف **لقطات شاشة وهمية** لتوضيح الواجهة ضمن هذا الملف قبل رفعه إلى GitHub؟
```
