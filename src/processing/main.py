"""
Main processing entrypoint (adds in needed merges, joins, etc.)
"""

import pandas as pd

from typing import Any

from .geo import load_and_prepare_geo
from .yelp import load_and_prepare_yelp
from .complaints import load_and_prepare_311
from .litter_index import load_and_prepare_litter_index


def load_data(data_dir: str = "data") -> dict[str, Any]:
    data_311 = load_and_prepare_311(f"{data_dir}/phi_311_no_info_request.csv")
    yelp = load_and_prepare_yelp(f"{data_dir}/philly_yelp_data.csv")
    litter = load_and_prepare_litter_index(f"{data_dir}/Litter_Index_Neighborhoods.csv")
    geo = load_and_prepare_geo(f"{data_dir}/philly_zipcodes.geojson")

    metrics_by_zip = yelp["by_zip"].merge(data_311["by_zip"], on="zip_code", how="left")
    metrics_by_zip["complaints"] = metrics_by_zip["complaints"].fillna(0)
    metrics_by_zip["complaints_per_restaurant"] = (
        metrics_by_zip["complaints"] / metrics_by_zip["n_restaurants"]
    )

    geo_with_metrics = geo["feature_properties"].merge(metrics_by_zip, on="zip_code", how="left")

    dataframes: dict[str, pd.DataFrame] = {
        "complaints_311": data_311["default"],
        "complaints_311_all": data_311["all"],
        "complaints_311_by_zip": data_311["by_zip"],
        "yelp": yelp["default"],
        "yelp_by_zip": yelp["by_zip"],
        "litter_index": litter["default"],
        "litter_by_division": litter["by_division"],
        "litter_trend": litter["trend"],
        "geo_features": geo["feature_properties"],
        "metrics_by_zip": metrics_by_zip,
        "geo_with_metrics": geo_with_metrics,
    }
    return {"dataframes": dataframes, "geojson": geo["default"]}
