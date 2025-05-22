# 🤖 ChartBuilder-Agent: AI Agent for Divisional Chart Generation (D1–D164)

**ChartBuilder-Agent** is a powerful AI-driven FastAPI microservice that computes **Vedic divisional charts (D-charts)** with high mathematical accuracy using the **Swiss Ephemeris (Lahiri Ayanamsha)**.  
Created by **Harshit Pandey**, this tool supports all charts from **D1 to D144**, and is ideal for both classical astrologers and AI-based spiritual applications.

---

## 🧐 What is This?

A fully encapsulated **astrological AI agent** that takes a user’s **birth date, time, and location**, and returns planetary placements in divisional charts like **D1 (Āśi), D9 (Navāmsha), D10 (Dashāmsha), D60 (Shashtyāmsha)** and more.  
Built for deterministic, verifiable output — optimized for pipelines, dashboards, or embedded astrology engines.

---

## 📜 Features

- 🥮 Accurate generation of D-charts from **D1 to D144**
- 🌍 Uses **Lahiri Ayanamsha** (sidereal)
- 🔭 Computes **Lagna, Rahu, and Ketu** with planetary positions
- ⚙️ Powered by **FastAPI** with OpenAPI Swagger interface
- 📆 JSON output designed for easy chaining and storage
- ☁️ Deployable on **Render, Railway, Docker**, or local environments

---

## 🗂 Supported Divisional Charts

| Chart | Sanskrit Name             | Purpose                    |
|-------|----------------------------|-----------------------------|
| D1    | Rāśi                      | Birth Chart (Physical)      |
| D2    | Horā                      | Wealth                      |
| D3    | Drekāṅa                  | Siblings                    |
| D4    | Chaturthāmsha             | Fortune, Property           |
| D5    | Pañchāmsha                | Fame                        |
| D6    | Shashthāmsha              | Enemies, Diseases           |
| D7    | Saptāmsha                 | Children                    |
| D9    | Navāmsha                  | Marriage, Dharma            |
| D10   | Dashāmsha                 | Career                      |
| D12   | Dvādashāmsha              | Parents                     |
| D16   | Shodashāmsha              | Luxuries, Vehicles          |
| D20   | Vimshāmsha                | Spiritual Growth            |
| D24   | Siddhāmsha                | Education                   |
| D27   | Bhamshāmsha               | Strength, Vitality          |
| D30   | Trimshāmsha               | Evils, Misfortunes          |
| D40   | Khavedāmsha               | Maternal Karma              |
| D45   | Akshavedāmsha             | Paternal Karma              |
| D60   | Shashtyāmsha              | Past Life Karma             |
| D108  | Ashtottarāmsha            | Higher Self Tendencies      |
| D144  | Dvichatvāriṁshāmsha       | Deep Karmic Seed            |

---

## 🛠 Tech Stack

- **FastAPI** – for REST API framework  
- **Pydantic** – for request schema validation  
- **Swiss Ephemeris (pyswisseph)** – for high-precision calculations  
- **Uvicorn** – ASGI server for performance & scalability

---

## 🚀 Running Locally

```bash
git clone https://github.com/YOUR_USERNAME/chartbuilder-agent.git
cd chartbuilder-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## ☁️ Deploy to Render (Free)

1. Push this repo to your **GitHub**
2. Go to 👉 [https://render.com](https://render.com)
3. Click **New Web Service**
4. Connect to your GitHub repo

### 🔧 Render Settings

| Setting           | Value                                                 |
|-------------------|-------------------------------------------------------|
| **Build Command** | `pip install -r requirements.txt`                     |
| **Start Command** | `uvicorn main:app --host=0.0.0.0 --port=$PORT`        |
| **Runtime**       | Python 3.11+                                          |
| **Instance Type** | Free Tier                                             |

---

## 🌐 Live API (Swagger UI)

Access the live OpenAPI UI to test it directly from your browser:

🔗 **[https://chartbuilder-agent.onrender.com/docs](https://chartbuilder-agent.onrender.com/docs)**

---

### 🦪 How to Test the API

1. Open: [https://chartbuilder-agent.onrender.com/docs](https://chartbuilder-agent.onrender.com/docs)
2. Click **POST /build-charts**
3. Click **"Try it out"**
4. Paste the following into the **Request Body**:

```json
{
  "dob": "1990-01-01",
  "tob": "12:00",
  "location": "Ujjain, India",
  "lat": 23.1765,
  "lon": 75.7885,
  "tz_offset": 5.5,
  "divisions": ["D1", "D9", "D60"]
}
```

5. Click **Execute**
6. The response will show the divisional chart results with Sanskrit chart names and planetary placements.

---

## 📚 References

- 📌 [Swiss Ephemeris](https://www.astro.com/swisseph)  
- 📌 Lahiri Ayanamsha  
- 📌 Parāśara Hora Śāstra  
- 📌 Phaladeepika – Mantreswara  
- 📌 Devakeralam (Chandrakala Nadi)  
- 📌 Jataka Parijata  

---

## 👤 Author

**Harshit Pandey**  
Astro-Architect • Cloud & AI Strategist  
🔗 [linkedin.com/in/pandeyharshit](https://linkedin.com/in/pandeyharshit)

---

## 📖 License

**MIT License** — Use freely, improve, contribute, or fork. No attribution required.
