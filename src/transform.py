import numpy as np
import pandas as pd

from config import settings


def _classify_zone(row: pd.Series) -> str:
    """Assign a shot to a court zone based on distance and type."""
    distance = row["SHOT_DISTANCE"]  # in feet
    is_three = row["SHOT_TYPE"] == "3PT Field Goal"

    if is_three:
        # corner threes sit at a shorter distance than above-the-break
        if distance <= settings.CORNER_THREE_DISTANCE + 1:
            return "Corner 3"
        return "Above the Break 3"

    if distance <= settings.RESTRICTED_AREA_RADIUS:
        return "Restricted Area"
    if distance <= 14:
        return "Paint / Short Mid-Range"
    return "Mid-Range"


def clean_shots(df: pd.DataFrame) -> pd.DataFrame:
    """Trim raw API columns down to what the pipeline needs and add zones."""
    keep = [
        "PLAYER_NAME", "TEAM_NAME", "GAME_DATE",
        "LOC_X", "LOC_Y", "SHOT_DISTANCE",
        "SHOT_TYPE", "SHOT_MADE_FLAG", "ACTION_TYPE",
    ]
    clean = df[keep].copy()

    # the API stores coordinates in tenths of a foot; convert to feet
    clean["LOC_X"] = clean["LOC_X"] / 10.0
    clean["LOC_Y"] = clean["LOC_Y"] / 10.0

    clean["ZONE"] = clean.apply(_classify_zone, axis=1)
    return clean


def zone_efficiency(df: pd.DataFrame) -> pd.DataFrame:
    """Compute attempts, makes, FG% and eFG% per zone."""
    grouped = df.groupby("ZONE")
    summary = grouped.agg(
        attempts=("SHOT_MADE_FLAG", "count"),
        makes=("SHOT_MADE_FLAG", "sum"),
    ).reset_index()

    summary["fg_pct"] = (summary["makes"] / summary["attempts"]).round(3)

    # effective FG% weights threes 1.5x. flag three-point zones by name.
    is_three_zone = summary["ZONE"].str.contains("3")
    three_makes = np.where(is_three_zone, summary["makes"] * 0.5, 0)
    summary["efg_pct"] = (
        (summary["makes"] + three_makes) / summary["attempts"]
    ).round(3)

    return summary.sort_values("attempts", ascending=False)