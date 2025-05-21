# 🤖 ChartBuilder-Agent: AI Agent for Divisional Chart Generation (D1–D164)

**ChartBuilder-Agent** is a powerful AI-powered FastAPI microservice that generates **Vedic divisional charts (D-charts)** with absolute mathematical accuracy using the **Swiss Ephemeris (Lahiri Ayanamsha)**. Designed by **Harshit Pandey**, this agent computes D1 to D144 charts, suitable for both traditional astrologers and modern AI pipelines.

---

## 🧠 What is This?

This is a **self-contained AI agent** that accepts a birth date, time, and location and returns Vedic divisional charts such as D1 (Rāśi), D9 (Navāmsha), D60 (Shashtyāmsha), etc., with all planetary positions including **Rahu, Ketu, and Lagna**. It is engineered for **deterministic, verifiable, and replicable output**, and ideal for AI-based astrology apps, research, or spiritual dashboards.

---

## 📜 Features

- 🧮 Computes accurate D-charts: D1 to D144 supported
- 🌍 Based on **Lahiri Ayanamsha** (sidereal)
- 🔭 Includes support for Lagna, Rahu, and Ketu
- ⚙️ FastAPI backend with OpenAPI Swagger UI
- 📦 Ready to deploy on Render / Railway / Docker
- 📂 JSON output suitable for chaining or database storage

---

## 🗂 Supported Divisional Charts

| Chart | Sanskrit Name                   | Purpose                 |
|-------|----------------------------------|--------------------------|
| D1    | Rāśi                            | Birth Chart (Body)      |
| D2    | Horā                            | Wealth                  |
| D3    | Drekkāṇa                        | Siblings                |
| D4    | Chaturthāmsha                   | Fortune, Property       |
| D5    | Pañchāmsha                      | Fame                    |
| D6    | Shashthāmsha                    | Diseases, Enemies       |
| D7    | Saptāmsha                       | Children                |
| D9    | Navāmsha                        | Marriage, Dharma        |
| D10   | Dashāmsha                       | Career                  |
| D12   | Dvādashāmsha                    | Parents                 |
| D16   | Shodashāmsha                    | Vehicles, Luxuries      |
| D20   | Vimshāmsha                      | Spiritual Growth        |
| D24   | Siddhāmsha                      | Education               |
| D27   | Bhamshāmsha                     | Strength                |
| D30   | Trimshāmsha                     | Evils, Misfortunes      |
| D40   | Khavedāmsha                     | Maternal Karma          |
| D45   | Akshavedāmsha                   | Paternal Karma          |
| D60   | Shashtyāmsha                    | Past Life Karma         |
| D108  | Ashtottarāmsha                  | Higher Self Tendencies  |
| D144  | Dvichatvāriṃshāmsha             | Deep Karmic Seed        |

---

## 🚀 Running Locally

```bash
git clone https://github.com/YOUR_USERNAME/chartbuilder-agent.git
cd chartbuilder-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

## ☁️ Deploy to Render (Free)

1. Push this repo to your GitHub
2. Go to 👉 [https://render.com](https://render.com)
3. Click **“New Web Service”**
4. Connect to your GitHub repo

### 🔧 Settings:

| Setting         | Value                                             |
|-----------------|---------------------------------------------------|
| **Build Command** | `pip install -r requirements.txt`               |
| **Start Command** | `uvicorn main:app --host=0.0.0.0 --port=$PORT`  |
| **Runtime**       | Python 3.11+                                    |
| **Instance Type** | Free Tier                                       |

---

## 🛠 Tech Stack

- **FastAPI** – for HTTP API framework  
- **Pydantic** – for input validation  
- **Swiss Ephemeris** (`pyswisseph`) – for planetary calculations  
- **Uvicorn** – ASGI server for deployment  

---

## 📚 References

- 📌 [Swiss Ephemeris](https://www.astro.com/swisseph)
- 📌 Lahiri Ayanamsha
- 📌 Parashara Hora Shastra (BPHS)
- 📌 Phaladeepika by Mantreswara
- 📌 Devakeralam (Chandrakala Nadi)
- 📌 Jataka Parijata

---

## 👤 Author

**Harshit Pandey**  
Astro-Architect | Cloud & AI Strategist  
🔗 [linkedin.com/in/pandeyharshit](https://linkedin.com/in/pandeyharshit)
