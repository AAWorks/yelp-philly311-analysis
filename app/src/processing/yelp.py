"""
Prep yelp data
"""

import pandas as pd

from .utils import normalize_zip_code


def load_and_prepare_yelp(path: str = "data/philly_yelp_data.csv") -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, low_memory=False)

    # tbd restaurants only
    # categories = df["categories"].fillna("").astype(str)
    # is_restaurant = categories.str.contains("Restaurant", case=False, na=False)
    # df.loc[is_restaurant].copy()

    df["zip_code"] = normalize_zip_code(df["postal_code"])
    df = df.dropna(subset=["zip_code"]).copy()

    df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce").fillna(0)
    df["stars"] = pd.to_numeric(df["stars"], errors="coerce")
    df["weighted_stars"] = df["stars"] * df["review_count"]

    by_zip = (
        df.groupby("zip_code", as_index=False)
        .agg(
            weighted_stars_sum=("weighted_stars", "sum"),
            review_count_sum=("review_count", "sum"),
            n_restaurants=("business_id", "nunique"),
        )
        .sort_values("zip_code")
        .reset_index(drop=True)
    )

    by_zip["yelp_rating_wtd"] = by_zip["weighted_stars_sum"] / by_zip["review_count_sum"].where(
        by_zip["review_count_sum"].gt(0)
    )
    by_zip = by_zip.drop(columns=["weighted_stars_sum", "review_count_sum"])

    return dict(
        default=df,
        by_zip=by_zip
    )
