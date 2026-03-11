"""
Strip yelp data down to Philly-only
"""

import pandas as pd


if __name__ == "__main__":
    chunks = pd.read_json(
        "data/yelp_academic_dataset_business.json",
        lines=True,
        chunksize=100_000
    )

    yelp_df = pd.concat(chunks, ignore_index=True)
    df2 = yelp_df.loc[yelp_df['city'] == 'Philadelphia'].copy()
    df2.to_csv('data/philly_yelp_data.csv', index=False)