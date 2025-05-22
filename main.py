from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import swisseph as swe
import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

app = FastAPI()

# Set Swiss Ephemeris path
swe.set_ephe_path("/usr/share/ephe")

# Supported divisional charts and their divisions per sign
DIVISION_RULES = {
    "D1": 1,
    "D2": 2,
    "D3": 3,
    "D4": 4,
    "D5": 5,
    "D6": 6,
    "D7": 7,
    "D8": 8,
    "D9": 9,
    "D10": 10,
    "D12": 12,
    "D16": 16,
    "D20": 20,
    "D24": 24,
    "D27": 27,
    "D30": 30,
    "D40": 40,
    "D45": 45,
    "D60": 60,
    "D81": 81,
    "D108": 108,
    "D144": 144
}

SANSKRIT_NAMES = {
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

class ChartInput(BaseModel):
    dob: str
    tob: str
    location: str
    divisions: List[str]


def get_location_details(place_name):
    geolocator = Nominatim(user_agent="chartbuilder-agent")
    location = geolocator.geocode(place_name)
    if not location:
        raise Exception("Location not found")
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
    timezone = pytz.timezone(timezone_str)
    now = datetime.datetime.now(timezone)
    offset = timezone.utcoffset(now).total_seconds() / 3600
    return round(location.latitude, 4), round(location.longitude, 4), round(offset, 2)


@app.post("/build-charts")
def build_div_charts(input: ChartInput):
    try:
        lat, lon, tz_offset = get_location_details(input.location)
        dt = datetime.datetime.strptime(f"{input.dob} {input.tob}", "%Y-%m-%d %H:%M")
        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0 - tz_offset)
        charts = {}

        planet_ids = {
            "SUN": swe.SUN,
            "MOON": swe.MOON,
            "MERCURY": swe.MERCURY,
            "VENUS": swe.VENUS,
            "MARS": swe.MARS,
            "JUPITER": swe.JUPITER,
            "SATURN": swe.SATURN,
            "RAHU": swe.MEAN_NODE,
            "KETU": swe.MEAN_NODE
        }

        for div in input.divisions:
            div_count = DIVISION_RULES.get(div)
            if not div_count:
                continue

            planets = {}
            for name, pid in planet_ids.items():
                lon_val, _ = swe.calc_ut(jd, pid)
                if name == "KETU":
                    lon_val = (swe.calc_ut(jd, swe.MEAN_NODE)[0] + 180) % 360
                sign = int((lon_val % 30) * div_count / 30)
                final_sign = int(((int(lon_val / 30) * div_count) + sign) / div_count) + 1
                final_sign = (final_sign - 1) % 12 + 1
                planets[name] = final_sign

            asc = swe.houses(jd, lat, lon)[0][0]
            asc_sign = int((asc % 30) * div_count / 30)
            final_asc = int(((int(asc / 30) * div_count) + asc_sign) / div_count) + 1
            final_asc = (final_asc - 1) % 12 + 1
            planets["LAGNA"] = final_asc

            charts[div] = {
                "sanskrit_name": SANSKRIT_NAMES.get(div, ""),
                "planets": planets
            }

        return {
            "input": {
                "dob": input.dob,
                "tob": input.tob,
                "location": input.location,
                "lat": lat,
                "lon": lon,
                "tz_offset": tz_offset,
                "divisions": input.divisions
            },
            "charts": charts,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
