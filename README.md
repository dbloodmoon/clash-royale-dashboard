# 👑 Clash Royale Clan Dashboard ⚔️

Un dashboard interactivo construido en Python con Streamlit para visualizar y analizar estadísticas en tiempo real de los miembros de clanes en Clash Royale, consumiendo la API oficial del juego.

> **Proyecto de Portafolio** desarrollado por [@dbloodmoon](https://github.com/dbloodmoon)

---

## ✨ Características

* **Buscador en Vivo**: Ingresa cualquier Tag de Clan oficial y obtén resultados al instante.
* **Métricas del Clan**: Total de miembros, promedio de copas y copas totales.
* **Tabla de Miembros**: Visualiza nombre, rol, copas, donaciones e inactividad de cada jugador.
* **Guerra de Clanes**: Tabla de participantes con datos de la River Race (fama, mazos usados).
* **Internacionalización**: Interfaz disponible en Español e Inglés (i18n).
* **Arquitectura OOP**: Cliente API orientado a objetos, fácil de escalar y mantener.

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| **Python 3.x** | Lenguaje principal |
| **Streamlit** | Interfaz web reactiva |
| **Requests** | Consumo de API REST |
| **python-dotenv** | Gestión segura de credenciales |
| **Pandas** | Manejo de DataFrames |

---

## 📁 Estructura del Proyecto

```
API/
├── app.py              # Interfaz web (Streamlit)
├── clash_client.py     # Cliente de la API de Clash Royale (OOP)
├── translations.py     # Sistema de internacionalización (i18n)
├── main.py             # Script de pruebas en consola
├── requirements.txt    # Dependencias del proyecto
├── .env                # Variables de entorno (NO incluido en el repo)
└── .gitignore          # Archivos excluidos de Git
```

---

## 🚀 Cómo ejecutar localmente

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/dbloodmoon/clash-royale-dashboard.git
   cd clash-royale-dashboard
   ```

2. **Crea un entorno virtual e instala las dependencias:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configura tus credenciales:**

   Crea un archivo `.env` en la raíz del proyecto con tu Token de desarrollador de Clash Royale (obtenible en [developer.clashroyale.com](https://developer.clashroyale.com/)):
   ```env
   CLASH_TOKEN=tu_token_aqui
   ```

4. **Arranca el Dashboard:**
   ```bash
   streamlit run app.py
   ```

---

## 📸 Preview

> *Próximamente: capturas del Dashboard*

---

## 📄 Licencia

Este proyecto es de código abierto bajo la licencia MIT.
