"""
Exploratory distribution/trend for Litter Index.
"""

import altair as alt
import pandas as pd

from ..common.theme import CHART_HEIGHT, CHART_WIDTH


def _prep_litter_by_division(litter_by_division: pd.DataFrame) -> pd.DataFrame:
    df = litter_by_division.copy()
    df["score_range"] = df["litter_score_max"] - df["litter_score_min"]
    df = df.dropna(subset=["division_num", "litter_score_mean", "litter_score_min", "litter_score_max"])
    return df

def build_litter_mean_vs_range_scatter(
    litter_by_division: pd.DataFrame,
    label_n: int = 10,
) -> alt.Chart:
    df = _prep_litter_by_division(litter_by_division)

    labels_df = df.nlargest(label_n, "score_range").copy()

    points = (
        alt.Chart(df)
        .mark_circle(opacity=0.75)
        .encode(
            x=alt.X(
                "litter_score_mean:Q",
                title="Average litter score across observed years",
            ),
            y=alt.Y(
                "score_range:Q",
                title="Historical score range (max - min)",
            ),
            size=alt.Size(
                "shape__area:Q",
                title="Division area",
                scale=alt.Scale(range=[40, 900]),
            ),
            tooltip=[
                alt.Tooltip("division_num:N", title="Division"),
                alt.Tooltip("litter_score_mean:Q", title="Mean score", format=".3f"),
                alt.Tooltip("litter_score_min:Q", title="Min score", format=".3f"),
                alt.Tooltip("litter_score_max:Q", title="Max score", format=".3f"),
                alt.Tooltip("score_range:Q", title="Range", format=".3f"),
                alt.Tooltip("n_years:Q", title="Observed years"),
                alt.Tooltip("shape__area:Q", title="Area", format=",.0f"),
            ],
        )
        .properties(
            width=CHART_WIDTH,
            height=CHART_HEIGHT,
        )
    )

    labels = (
        alt.Chart(labels_df)
        .mark_text(dx=8, dy=-6, fontSize=11)
        .encode(
            x="litter_score_mean:Q",
            y="score_range:Q",
            text="division_num:N",
        )
    )

    return points + labels


def build_litter_range_dumbbell(
    litter_by_division: pd.DataFrame,
    top_n: int = 12,
) -> alt.Chart:
    df = _prep_litter_by_division(litter_by_division)
    df = df.sort_values("score_range", ascending=False).head(top_n).copy()

    order = df["division_num"].tolist()

    rules = (
        alt.Chart(df)
        .mark_rule(strokeWidth=3)
        .encode(
            y=alt.Y("division_num:N", sort=order, title="Division"),
            x=alt.X("litter_score_min:Q", title="Litter score"),
            x2="litter_score_max:Q",
            tooltip=[
                alt.Tooltip("division_num:N", title="Division"),
                alt.Tooltip("litter_score_min:Q", title="Min score", format=".3f"),
                alt.Tooltip("litter_score_mean:Q", title="Mean score", format=".3f"),
                alt.Tooltip("litter_score_max:Q", title="Max score", format=".3f"),
                alt.Tooltip("score_range:Q", title="Range", format=".3f"),
                alt.Tooltip("n_years:Q", title="Observed years"),
            ],
        )
    )

    min_points = (
        alt.Chart(df)
        .mark_circle(size=90)
        .encode(
            y=alt.Y("division_num:N", sort=order, title="Division"),
            x=alt.X("litter_score_min:Q", title="Litter score"),
            color=alt.value("#4C78A8"),
        )
    )

    max_points = (
        alt.Chart(df)
        .mark_circle(size=90)
        .encode(
            y=alt.Y("division_num:N", sort=order, title="Division"),
            x=alt.X("litter_score_max:Q", title="Litter score"),
            color=alt.value("#E45756"),
        )
    )

    mean_points = (
        alt.Chart(df)
        .mark_circle(size=70)
        .encode(
            y=alt.Y("division_num:N", sort=order, title="Division"),
            x=alt.X("litter_score_mean:Q", title="Litter score"),
            color=alt.value("#72B7B2"),
        )
    )

    return (rules + min_points + max_points + mean_points).properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT,
    )
