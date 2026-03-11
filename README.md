# 👑 Clash Royale - Clan Stats Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://clash-royale-dashboard.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.55-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

An interactive web dashboard built with **Python** and **Streamlit** to visualize and analyze **Clash Royale** clan statistics in real time using the official Supercell API.

> 🔗 **Live Demo:** [clash-royale-dashboard.streamlit.app](https://clash-royale-dashboard.streamlit.app)

---

## ✨ Features

- 🔍 **Live Clan Search** — Enter any official Clan Tag and get instant results.
- 📊 **Clan KPIs** — Total members, average trophies, and total trophies at a glance.
- 👥 **Members Table** — Name, role, trophies, donations, and inactivity tracker for every player.
- ⚔️ **Clan War (River Race)** — Participation data including fame, boat attacks, and decks used.
- 🌐 **Bilingual (i18n)** — Full interface available in English and Spanish.
- 🏗️ **OOP Architecture** — Clean, modular API client designed for scalability.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.x** | Core language |
| **Streamlit** | Reactive web UI framework |
| **Requests** | REST API consumption |
| **python-dotenv** | Secure credential management |
| **Pandas** | DataFrame handling |
| **Clash Royale API** | Official Supercell data source |

---

## 📁 Project Structure

```
├── app.py              # Web interface (Streamlit)
├── clash_client.py     # Clash Royale API client (OOP)
├── translations.py     # Internationalization system (i18n)
├── requirements.txt    # Project dependencies
├── .env                # Environment variables (NOT in repo)
└── .gitignore          # Git excluded files
```

---

## 🚀 Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dbloodmoon/clash-royale-dashboard.git
   cd clash-royale-dashboard
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up your credentials:**

   Create a `.env` file in the project root with your Clash Royale Developer Token (get it at [developer.clashroyale.com](https://developer.clashroyale.com/)):
   ```env
   CLASH_TOKEN=your_token_here
   ```

4. **Launch the Dashboard:**
   ```bash
   streamlit run app.py
   ```

---

## 📸 Preview

<img width="1280" height="720" alt="image" src="https://github.com/user-attachments/assets/5dd9c381-d5da-4aa6-8634-eebcd8671e84" />

---

## 👨‍💻 Author

Developed by **[@dbloodmoon](https://github.com/dbloodmoon)** — B.S Computer Science.

## 📄 License

This project is open source under the [MIT License](LICENSE).
