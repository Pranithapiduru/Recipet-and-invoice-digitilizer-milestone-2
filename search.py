import pandas as pd


def search_receipts(df: pd.DataFrame, keyword: str):
    if df.empty or not keyword:
        return df

    return df[df["merchant"].str.contains(keyword, case=False, na=False)]
