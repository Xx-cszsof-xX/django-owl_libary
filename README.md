# 🦉 Django Owl Library

A **Django Owl Library** egy webes könyvkiadó rendszer, amely lehetővé teszi könyvek böngészését, kosárba helyezését, felhasználói profilkezelést és adminisztratív tartalomkezelést.  
A projekt a Django keretrendszerre épül, és követi az MVC architektúrát. A rendszer magyar nyelvű felhasználói felülettel rendelkezik.

---

## 🎯 Főbb funkciók

- 📚 Könyvek listázása (címmel, szerzővel, kiadási dátummal, borítóval)
- 🔍 Keresés funkció a könyvek és a munkatársak között
- 🛒 Kosár funkció (mennyiség kezelése, végösszeg számítás)
- 👤 Felhasználói profil (saját bio és születési dátum megadása)
- 🖼️ Profilkép feltöltés
- 🧾 Adminfelület (Django admin)
- 🌐 Többnyelvűség támogatása (nyelvválasztó)
- 📦 Statisztikus és média fájlok kezelése (`static`, `media`)

---

## 📁 Projekt Felépítés

```
webbeadando/
├── kiado/
│   ├── kiado/               # Fő Django projekt (settings, urls, wsgi)
│   └── main_kiado/          # Fő alkalmazás logikával, modellekkel, nézetekkel
│       ├── locale/          # Fordítási fájlok
│       ├── media/           # Feltöltött fájlok
│       ├── static/          # CSS, JS, képek
│       ├── templates/       # HTML sablonok
│       ├── templatetags/    # Egyedi Django template tag-ek
│       ├── context_processors.py
│       ├── middleware.py
│       ├── signals.py
│       ├── models.py, views.py, forms.py, admin.py, etc.
├── requirements.txt         # Függőségek listája
```

---

## ⚙️ Telepítés és futtatás

1. **Virtuális környezet (ajánlott)**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

2. **Függőségek telepítése**

```bash
pip install -r requirements.txt
```

3. **Migrációk futtatása**

```bash
python manage.py migrate
```

4. **Szerver indítása**

```bash
python manage.py runserver
```

📍 Az alkalmazás elérhető: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧠 Architektúra

Az alkalmazás a Django által követett MTV (Model–Template–View) struktúrát alkalmazza:

- **Model**: Adatbázisstruktúrák (`models.py`)
- **Template**: Felhasználói felület HTML sablonjai
- **View**: Üzleti logika (`views.py`, `forms.py`, `context_processors.py`)

Továbbá saját middleware és signals is alkalmazásra kerültek, amelyek a működés testreszabását segítik.

---





## 👀 Képernyőképek

A projekt tartalmaz képernyőképeket a főbb funkciókról, többek között:
- Könyvek listája kosárba helyezési lehetőséggel
- Kosár nézet
- Felhasználói profil és profil szerkesztés

---
![Képernyőkép 2025-03-27 182215](https://github.com/user-attachments/assets/d86ff4d3-acb6-4a31-8052-166728c530fe)
![Képernyőkép 2025-03-27 182153](https://github.com/user-attachments/assets/5ca173f5-605f-4c60-a3db-c16ba97988cc)
![Képernyőkép 2025-03-27 182134](https://github.com/user-attachments/assets/b6e1ca11-fe7e-4251-9aed-cc6186e8a4d4)
![Képernyőkép 2025-03-27 182114](https://github.com/user-attachments/assets/f74a4fdb-b1fc-4fd9-96a7-f70490760611)
