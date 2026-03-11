"""
Shared encoding helpers.
"""

import altair as alt


def zip_tooltip_fields(extra_fields: list[str] | None = None) -> list[alt.Tooltip]:
    tooltips = [alt.Tooltip("properties.zip_code:N", title="ZIP")]
    for field in extra_fields or []:
        tooltips.append(alt.Tooltip(field))
    return tooltips
