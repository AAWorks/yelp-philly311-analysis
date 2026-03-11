"""
Prep 311 dataset
"""

import pandas as pd

from .utils import normalize_zip_code


KEEP_TERMS = [
    "graffiti",
    "rodent",
    "sanitation",
    "trash",
    "garbage",
    "litter",
    "rubbish",
    "dump",
    "recycle",
    "outage"
]

DATE_COLUMNS = [
    "requested_datetime",
    "updated_datetime",
    "expected_datetime",
    "closed_datetime",
]


def categorize_311_service(service_name: str) -> str:
    s = (service_name or "").lower()

    if "rodent" in s or "rat" in s or "mouse" in s:
        return "rodent"
    if "graffiti" in s:
        return "graffiti"
    if "outage" in s:
        return "light outage"
    if any(
        term in s for term in KEEP_TERMS
    ):
        return "sanitation/trash"
    return "other"


def load_and_prepare_311(path: str = "data/phi_311_no_info_request.csv") -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, low_memory=False)

    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    df["zip_code"] = normalize_zip_code(df["zipcode"])
    df = df.dropna(subset=["zip_code"]).copy()

    df["service_name"] = df["service_name"].fillna("").astype(str).str.lower()
    df["complaint_bucket"] = df["service_name"].map(categorize_311_service)

    clean = df.loc[
        df["service_name"].str.contains(
            "|".join(KEEP_TERMS),
            na=False
        )
    ].copy()

    by_zip = (
        clean.groupby("zip_code", as_index=False)
        .size()
        .rename(columns={"size": "complaints"})
        .sort_values("zip_code")
        .reset_index(drop=True)
    )

    return dict(
        all=df,
        default=clean,
        by_zip=by_zip
    )
