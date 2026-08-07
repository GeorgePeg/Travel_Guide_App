# 🌍 Travel Guide Web App

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=for-the-badge&logo=leaflet&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

Ένας πλήρης διαδραστικός οδηγός ταξιδιών χτισμένος με **Python** και **Django**. Επιτρέπει σε χρήστες να αναζητούν προορισμούς, να βλέπουν αξιοθέατα που υπάρχουν στον προορισμό αυτό, να κρατούν σημειώσεις και να οργανώνουν τα ταξίδια τους.

---

## 🛠️ Τεχνολογίες & Εργαλεία

| Κατηγορία | Τεχνολογία | Description |
| :--- | :--- | :--- |
| **Backend** | Python & Django 5.x | Core framework, ORM, Auth & Admin Panel |
| **Frontend** | HTML5, CSS3, JavaScript | Django Templates & Interactive UI elements |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) | Αποθήκευση χρηστών, προορισμών & κριτικών |
| **Maps & GIS** | Leaflet.js | Open-source διαδραστικοί χάρτες & πινέζες |
| **Tooling** | Git, Webhint (`.hintrc`) | Version control & Linter |

---

## 🚀 Εγκατάσταση & Εκτέλεση

### 1. Clone το Repository

\`\`\`bash

cd travel-guide

\`\`\`

### 2. Δημιουργία & Ενεργοποίηση Virtual Environment

\`\`\`bash
python -m venv venv

## Σε Linux/macOS

source venv/bin/activate

## Σε Windows

venv\Scripts\activate

\`\`\`

### 3. Εγκατάσταση Εξαρτήσεων

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Εκτέλεση Migrations & Δημιουργία Admin

\`\`\`bash
python manage.py migrate
python manage.py createsuperuser
\`\`\`

### 5. Εκκίνηση του Server

\`\`\`bash
python manage.py runserver
\`\`\`

Επισκεφθείτε την εφαρμογή στο: `http://127.0.0.1:8000/`.
