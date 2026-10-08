# src/f1/data.py
import fastf1
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = ROOT / ".fastf1_cache"
CACHE_DIR.mkdir(exist_ok=True)

LAP_COLUMNS = ["Driver", "Team", "LapNumber", "LapTime", "Stint", "Compound", "TyreLife", "FreshTyre", "Position", "PitInTime", "PitOutTime", "TrackStatus", "IsAccurate"]
WEATHER_COLUMNS = ["AirTemp", "TrackTemp", "Humidity", "WindSpeed", "Rainfall"]

def load_race_laps(year: int, round_number: int) -> pd.DataFrame:
    fastf1.Cache.enable_cache(CACHE_DIR)
    session = fastf1.get_session(year, round_number, "R")
    session.load(telemetry=False, weather=True, messages=False)
    
    laps = session.laps[LAP_COLUMNS].copy()
    laps["LapTime"] = laps["LapTime"].dt.total_seconds()
    
    laps["IsPitInLap"] = laps["PitInTime"].notna()
    laps["IsPitOutLap"] = laps["PitOutTime"].notna()
    laps = laps.drop(columns=["PitInTime", "PitOutTime"])
    
    weather = session.laps.get_weather_data().reset_index(drop=True)
    weather = weather[WEATHER_COLUMNS]
    
    laps = laps.reset_index(drop=True)
    laps = pd.concat([laps, weather], axis=1)
    
    assert len(laps) == len(weather)
    
    laps["Year"] = year
    laps["Round"] = round_number
    laps["Event"] = session.event["EventName"]
    
    return laps
    
    
    
