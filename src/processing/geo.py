"""
Prep Philly geojson data
"""

import json
from typing import Any

import pandas as pd

from .utils import normalize_zip_code


def load_and_prepare_geo(path: str = "data/philly_zipcodes.geojson") -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    records: list[dict[str, Any]] = []
    for idx, feature in enumerate(geojson_data.get("features", [])):
        props = feature.get("properties", {}) or {}
        record = {"feature_id": idx, **props}
        records.append(record)

    properties = pd.DataFrame(records)
    properties.columns = [str(col).strip().lower() for col in properties.columns]
    properties["zip_code"] = normalize_zip_code(properties["code"])

    # let geoshape lookups use properties.zip_code directly
    for feature in geojson_data.get("features", []):
        props = feature.setdefault("properties", {})
        props["zip_code"] = str(props.get("CODE"))

    return dict(
        default=geojson_data,
        feature_properties=properties,
        zip_source_column='code',
    )


if __name__ == "__main__":
    load_and_prepare_geo()
