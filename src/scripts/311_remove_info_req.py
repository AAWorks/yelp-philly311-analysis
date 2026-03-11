"""
Remove info-request so 311 dataset can be uploaded to github
"""

import pandas as pd


if __name__ == "__main__":
    df = pd.read_csv("data/phi_311.csv")
    df2 = df.loc[df['service_name'] != 'Information Request'].copy()
    df2.to_csv("data/phi_311_no_info_request.csv", index=False)
