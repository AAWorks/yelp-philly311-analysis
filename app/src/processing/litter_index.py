"""
Prep litter index df
"""

import pandas as pd


def load_and_prepare_litter_index(path: str = "data/Litter_Index_Neighborhoods.csv") -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, low_memory=False)
    df.columns = [col.replace("\ufeff", "").strip().lower() for col in df.columns]

    numeric_cols = ["division_num", "year", "division_score", "shape__area", "shape__length"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["division_num", "year"]).copy()
    df["division_num"] = df["division_num"].astype("int64")
    df["year"] = df["year"].astype("int64")

    latest_year = int(df["year"].max())
    latest = df.loc[df["year"].eq(latest_year)].copy()

    by_division = (
        df.groupby("division_num", as_index=False)
        .agg(
            litter_score_mean=("division_score", "mean"),
            litter_score_min=("division_score", "min"),
            litter_score_max=("division_score", "max"),
            n_years=("year", "nunique"),
            shape__area=("shape__area", "first"),
            shape__length=("shape__length", "first"),
        )
        .sort_values("division_num")
        .reset_index(drop=True)
    )

    year_min = int(df["year"].min())
    year_max = int(df["year"].max())
    earliest = (
        df.loc[df["year"].eq(year_min), ["division_num", "division_score"]]
        .rename(columns={"division_score": "division_score_earliest"})
        .copy()
    )
    latest_scores = (
        df.loc[df["year"].eq(year_max), ["division_num", "division_score"]]
        .rename(columns={"division_score": "division_score_latest"})
        .copy()
    )
    trend = earliest.merge(latest_scores, on="division_num", how="outer")
    trend["division_score_delta"] = trend["division_score_latest"] - trend["division_score_earliest"]

    # default is latest year (not looking to look at change over time)
    return dict(
        default=latest,
        by_division=by_division,
        trend=trend
    )
