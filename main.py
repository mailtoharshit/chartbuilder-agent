from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
import swisseph as swe
import os

app = FastAPI(title="ChartBuilder-Agent (Accurate Sidereal Ephemeris)")

class ChartRequest(BaseModel):
    dob: str
    tob: str
    location: str
    lat: float
    lon: float
    tz_offset: float
    divisions: List[str]

DIVISIONAL_CHART_NAMES = {
    "D1": "Rāśi (Birth Chart)",
    "D2": "Horā (Wealth)",
    "D3": "Drekkāṇa (Siblings)",
    "D4": "Chaturthāmsha (Fortune/Property)",
    "D5": "Pañchāmsha (Fame)",
    "D6": "Shashthāmsha (Enemies/Diseases)",
    "D7": "Saptāmsha (Children)",
    "D8": "Ashtāmsha (Longevity)",
    "D9": "Navāmsha (Marriage)",
    "D10": "Dashāmsha (Career)",
    "D11": "Ekādashāmsha (Power/Community)",
    "D12": "Dvādashāmsha (Parents)",
    "D16": "Shodashāmsha (Vehicles/Luxuries)",
    "D20": "Vimshāmsha (Spiritual Progress)",
    "D24": "Siddhāmsha (Education)",
    "D27": "Bhamshāmsha (Strength)",
    "D30": "Trimshāmsha (Evils)",
    "D40": "Khavedāmsha (Maternal Karma)",
    "D45": "Akshavedāmsha (Paternal Karma)",
    "D60": "Shashtyāmsha (Past Life Karma)",
    "D81": "Navanavāmsha (Subtle Evolution)",
    "D108": "Ashtottarāmsha (Higher Self Tendencies)",
    "D144": "Dvichatvāriṃshāmsha (Deep Karmic Seed)"
}

VEDIC_PLANETS = {
    'SUN': swe.SUN,
    'MOON': swe.MOON,
    'MERCURY': swe.MERCURY,
    'VENUS': swe.VENUS,
    'MARS': swe.MARS,
    'JUPITER': swe.JUPITER,
    'SATURN': swe.SATURN,
    'RAHU': swe.MEAN_NODE
}

swe.set_ephe_path(os.getcwd())
swe.set_sid_mode(swe.SIDM_LAHIRI)

class ChartBuilder:
    def __init__(self, dob: str, tob: str, lat: float, lon: float, tz_offset: float):
        try:
            local_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
            utc_dt = local_dt - timedelta(hours=tz_offset)
            self.jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60)
            self.lat = lat
            self.lon = lon
            swe.set_topo(lon, lat, 0)
        except ValueError:
            raise ValueError("Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time.")

    def get_planet_positions(self) -> Dict[str, float]:
        positions = {}
        for name, code in VEDIC_PLANETS.items():
            pos, _ = swe.calc(self.jd, code, flag=swe.FLG_SIDEREAL)
            positions[name] = pos[0]

        positions['KETU'] = (positions['RAHU'] + 180) % 360
        houses, _ = swe.houses(self.jd, self.lat, self.lon)
        positions['LAGNA'] = houses[0]

        return positions

    def calculate_navamsa(self, lon):
        rasi = int(lon // 30)
        deg = lon % 30
        pada = int(deg // 3.3333)
        return ((rasi * 9 + pada) % 12) + 1

    def calculate_saptamsa(self, lon):
        sign = int(lon // 30)
        deg_in_sign = lon % 30
        pada = int(deg_in_sign // (30 / 7))
        if (sign + 1) % 2 == 1:
            result_sign = (sign + pada) % 12
        else:
            result_sign = (sign + 6 - pada) % 12
        return result_sign + 1

    def calculate_division(self, lon: float, division: int, chart_name: str) -> int:
        sign = int(lon // 30)
        degree_in_sign = lon % 30

        if chart_name == "D2":
            return 5 if degree_in_sign < 15 else 4 if sign % 2 == 0 else 5

        if chart_name == "D3":
            return ((sign * 3 + int(degree_in_sign // 10)) % 12) + 1

        if chart_name == "D7":
            return self.calculate_saptamsa(lon)

        if chart_name == "D9":
            return self.calculate_navamsa(lon)

        if chart_name == "D10":
            part = int(degree_in_sign // (30 / 10))
            return ((sign + part) % 12) + 1 if (sign + 1) % 2 == 1 else ((8 + part) % 12) + 1

        if chart_name == "D30":
            if degree_in_sign < 5:
                return 2 if sign % 2 == 0 else 8
            elif degree_in_sign < 10:
                return 6 if sign % 2 == 0 else 12
            elif degree_in_sign < 18:
                return 10 if sign % 2 == 0 else 4
            elif degree_in_sign < 25:
                return 12 if sign % 2 == 0 else 6
            else:
                return 8 if sign % 2 == 0 else 2

        if chart_name == "D60":
            return int(lon // 0.5) % 12 + 1

        part_size = 30 / division
        part = int(degree_in_sign // part_size)
        return ((sign * division + part) % 12) + 1

    def generate(self, requested_divs: List[str]) -> Dict[str, Dict[str, Dict[str, int]]]:
        positions = self.get_planet_positions()
        charts = {}
        for div in requested_divs:
            if not div.startswith("D") or not div[1:].isdigit():
                continue
            division_number = int(div[1:])
            if div not in DIVISIONAL_CHART_NAMES:
                continue
            chart = {planet: self.calculate_division(lon, division_number, div) for planet, lon in positions.items()}
            charts[div] = {
                "sanskrit_name": DIVISIONAL_CHART_NAMES[div],
                "planets": chart
            }
        return charts

@app.post("/build-charts")
def build_div_charts(payload: ChartRequest):
    try:
        builder = ChartBuilder(
            dob=payload.dob,
            tob=payload.tob,
            lat=payload.lat,
            lon=payload.lon,
            tz_offset=payload.tz_offset
        )
        result = builder.generate(payload.divisions)
        return {
            "input": payload.dict(),
            "charts": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
