from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
CHARTS_DIR = BASE_DIR / "outputs" / "charts"

SEASON = "2023-24"
SEASON_TYPE = "Regular Season"  

PLAYER_NAME = "Stephen Curry"
PLAYER_ID = 201939

TEAM_NAME = "Golden State Warriors"
TEAM_ID = 1610612744

REQUEST_TIMEOUT = 30 
USE_CACHE = True  

THREE_POINT_DISTANCE = 23.75     
CORNER_THREE_DISTANCE = 22.0
RESTRICTED_AREA_RADIUS = 4.0