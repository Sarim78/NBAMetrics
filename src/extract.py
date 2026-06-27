import time
from pathlib import Path

import pandas as pd
from nba_api.stats.endpoints import shotchartdetail

from config import settings


def _cache_path() -> Path:
    """Build the raw cache filename for the current target."""
    name = settings.PLAYER_NAME.replace(" ", "_")
    season = settings.SEASON.replace("-", "")
    return settings.RAW_DIR / f"shots_{name}_{season}.csv"


def fetch_shots() -> pd.DataFrame:
    settings.RAW_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = _cache_path()

    if settings.USE_CACHE and cache_file.exists():
        print(f"[extract] loading cached shots from {cache_file.name}")
        return pd.read_csv(cache_file)

    print(f"[extract] requesting shots for {settings.PLAYER_NAME} ({settings.SEASON})")
    response = shotchartdetail.ShotChartDetail(
        team_id=0,                       # 0 = all teams the player was on
        player_id=settings.PLAYER_ID,
        season_nullable=settings.SEASON,
        season_type_all_star=settings.SEASON_TYPE,
        context_measure_simple="FGA",    # every field goal attempt
        timeout=settings.REQUEST_TIMEOUT,
    )

    # be polite to the API
    time.sleep(1)

    df = response.get_data_frames()[0]
    df.to_csv(cache_file, index=False)
    print(f"[extract] cached {len(df)} shots to {cache_file.name}")
    return df


if __name__ == "__main__":
    fetch_shots()