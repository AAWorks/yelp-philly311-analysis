"""
Shared dataframe transforms used by multiple charts.
"""

import pandas as pd
import numpy as np

def add_mismatch_score(metrics_by_zip: pd.DataFrame) -> pd.DataFrame:
    df = metrics_by_zip.copy()

    complaints_std = df["complaints_per_restaurant"].std(ddof=0)
    rating_std = df["yelp_rating_wtd"].std(ddof=0)

    if complaints_std == 0 or pd.isna(complaints_std):
        df["z_complaints_burden"] = 0.0
    else:
        df["z_complaints_burden"] = (
            df["complaints_per_restaurant"] - df["complaints_per_restaurant"].mean()
        ) / complaints_std

    if rating_std == 0 or pd.isna(rating_std):
        df["z_yelp_rating"] = 0.0
    else:
        df["z_yelp_rating"] = (df["yelp_rating_wtd"] - df["yelp_rating_wtd"].mean()) / rating_std

    df["mismatch_311_vs_yelp"] = df["z_yelp_rating"] - df["z_complaints_burden"]
    return df

def get_top_mismatch_zips(
    metrics_by_zip: pd.DataFrame,
    min_restaurants: int = 3,
    top_n_each: int = 5,
) -> pd.DataFrame:
    df = add_mismatch_score(metrics_by_zip)
    df = df.loc[df["n_restaurants"] >= min_restaurants].copy()

    pos = (
        df.nlargest(top_n_each, "mismatch_311_vs_yelp")
        .copy()
        .assign(mismatch_group="Yelp higher than complaints predict")
    )

    neg = (
        df.nsmallest(top_n_each, "mismatch_311_vs_yelp")
        .copy()
        .assign(mismatch_group="Yelp lower than complaints predict")
    )

    top = pd.concat([pos, neg], ignore_index=True)
    top["abs_mismatch"] = top["mismatch_311_vs_yelp"].abs()
    return top


def classify_complaint_detail(subject: str, service_name: str) -> str:
    s = f"{subject or ''} {service_name or ''}".lower()

    if "illegal dumping" in s or "dump" in s:
        return "Illegal dumping"
    if "rubbish" in s or "recycl" in s:
        return "Trash / recycling"
    if "trash" in s or "garbage" in s or "sanitation" in s or "litter" in s:
        return "Trash / recycling"
    if "street light" in s or "outage" in s or "lighting" in s:
        return "Lighting"
    if "graffiti" in s:
        return "Graffiti"
    if "rodent" in s or "rat" in s or "mouse" in s:
        return "Rodents"
    if "abandoned vehicle" in s or "abandoned automobile" in s:
        return "Abandoned vehicle"
    return "Other"


def category_tokens(categories: str) -> set[str]:
    if pd.isna(categories) or not categories:
        return set()
    return {token.strip() for token in str(categories).split(",") if token.strip()}


def is_restaurant_business(categories: str) -> bool:
    tokens = category_tokens(categories)

    if "Restaurants" in tokens:
        return True

    for _, tag_set in RESTAURANT_TYPE_RULES:
        if tokens & tag_set:
            return True

    return False


def classify_restaurant_type(categories: str) -> str:
    tokens = category_tokens(categories)

    for label, tag_set in RESTAURANT_TYPE_RULES:
        if tokens & tag_set:
            return label

    if is_restaurant_business(categories):
        specific_tokens = [t for t in tokens if t not in GENERIC_NON_TYPE_TAGS]
        if specific_tokens:
            return "Other restaurant"

    return np.nan


def _prepare_restaurant_type_panel_df(
    metrics_by_zip: pd.DataFrame,
    yelp_df: pd.DataFrame,
    min_restaurants: int = 3,
    top_n_each: int = 5,
    min_type_count: int = 2,
    max_types: int = 10,
) -> tuple[pd.DataFrame, list[str]]:
    top = get_top_mismatch_zips(
        metrics_by_zip,
        min_restaurants=min_restaurants,
        top_n_each=top_n_each,
    )[["zip_code", "mismatch_group", "mismatch_311_vs_yelp"]].copy()


    yelp = prepare_restaurant_type_df(yelp_df)
    yelp = yelp.loc[yelp["zip_code"].isin(top["zip_code"])].copy()

    if yelp.empty or top.empty:
        return pd.DataFrame(), []

    type_order = get_restaurant_type_options(
        metrics_by_zip,
        yelp_df,
        min_restaurants=min_restaurants,
        top_n_each=top_n_each,
        min_type_count=min_type_count,
    )

    if max_types is not None:
        type_order = type_order[:max_types]

    totals = (
        yelp.groupby("zip_code", as_index=False)
        .agg(
            total_restaurants=("business_id", "nunique"),
            total_reviews=("review_count", "sum"),
            overall_zip_rating=("stars", "mean"),
        )
    )

    by_type = (
        yelp.loc[yelp["restaurant_type"].isin(type_order)]
        .groupby(["zip_code", "restaurant_type"], as_index=False)
        .agg(
            type_restaurants=("business_id", "nunique"),
            type_reviews=("review_count", "sum"),
            type_avg_rating=("stars", "mean"),
        )
    )

    all_pairs = pd.MultiIndex.from_product(
        [top["zip_code"].tolist(), type_order],
        names=["zip_code", "restaurant_type"],
    ).to_frame(index=False)

    plot_df = (
        all_pairs.merge(top, on="zip_code", how="left")
        .merge(totals, on="zip_code", how="left")
        .merge(by_type, on=["zip_code", "restaurant_type"], how="left")
    )

    plot_df["type_restaurants"] = plot_df["type_restaurants"].fillna(0)
    plot_df["type_reviews"] = plot_df["type_reviews"].fillna(0)
    plot_df["type_avg_rating"] = plot_df["type_avg_rating"].fillna(np.nan)
    plot_df["type_share"] = plot_df["type_restaurants"] / plot_df["total_restaurants"]

    return plot_df, type_order


def get_restaurant_type_options(
    metrics_by_zip: pd.DataFrame,
    yelp_df: pd.DataFrame,
    min_restaurants: int = 3,
    top_n_each: int = 5,
    min_type_count: int = 2,
) -> list[str]:
    top = get_top_mismatch_zips(
        metrics_by_zip,
        min_restaurants=min_restaurants,
        top_n_each=top_n_each,
    )

    top_zips = set(top["zip_code"].tolist())

    yelp = prepare_restaurant_type_df(yelp_df)
    yelp = yelp.loc[yelp["zip_code"].isin(top_zips)].copy()

    counts = (
        yelp.groupby("restaurant_type")["business_id"]
        .nunique()
        .sort_values(ascending=False)
    )

    options = counts.loc[counts >= min_type_count].index.tolist()

    if "Other restaurant" in options:
        options.remove("Other restaurant")

    if not options:
        options = counts.index.tolist()

    return options

def prepare_restaurant_type_df(yelp_df: pd.DataFrame) -> pd.DataFrame:
    yelp = yelp_df.copy()
    yelp["stars"] = pd.to_numeric(yelp["stars"], errors="coerce")
    yelp["review_count"] = pd.to_numeric(yelp["review_count"], errors="coerce").fillna(0)

    yelp = yelp.loc[yelp["categories"].apply(is_restaurant_business)].copy()
    yelp["restaurant_type"] = yelp["categories"].apply(classify_restaurant_type)

    yelp = yelp.dropna(subset=["restaurant_type", "zip_code", "business_id"])
    return yelp

RESTAURANT_TYPE_RULES = [
    ("Pizza", {"Pizza"}),
    ("Italian", {"Italian"}),
    ("Chinese", {"Chinese"}),
    ("Japanese", {"Japanese", "Sushi Bars", "Ramen"}),
    ("Seafood", {"Seafood"}),
    ("American", {"American (Traditional)", "American (New)"}),
    ("Fast Food / Burgers", {"Fast Food", "Burgers", "Hot Dogs", "Chicken Wings"}),
    ("Sandwiches / Deli", {"Sandwiches", "Delis", "Cheesesteaks"}),
    ("Coffee / Bakery", {"Coffee & Tea", "Cafes", "Bakeries", "Desserts", "Bubble Tea"}),
    ("Bars / Pub Food", {"Bars", "Cocktail Bars", "Pubs", "Sports Bars", "Beer Bar", "Wine Bars", "Brewpubs"}),
]


GENERIC_NON_TYPE_TAGS = {
    "Restaurants",
    "Food",
    "Nightlife",
    "Bars",
    "Shopping",
    "Event Planning & Services",
    "Hotels & Travel",
    "Arts & Entertainment",
    "Local Services",
    "Home Services",
    "Beauty & Spas",
    "Automotive",
}
