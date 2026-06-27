from pathlib import Path
import pandas as pd
from config import settings

def _slug() -> str:
    name = settings.PLAYER_NAME.replace(" ", "_")
    season = settings.SEASON.replace("-", "")
    return f"{name}_{season}"

def save_processed(shots: pd.DataFrame, zones: pd.DataFrame) -> dict[str, Path]:
    """Write the cleaned shot table and zone summary as CSVs.

    Returns a dict of the paths written, for logging.
    """
    settings.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    shots_path = settings.PROCESSED_DIR / f"shots_clean_{_slug()}.csv"
    zones_path = settings.PROCESSED_DIR / f"zone_summary_{_slug()}.csv"

    shots.to_csv(shots_path, index=False)
    zones.to_csv(zones_path, index=False)

    print(f"[load] wrote {shots_path.name} and {zones_path.name}")
    return {"shots": shots_path, "zones": zones_path}