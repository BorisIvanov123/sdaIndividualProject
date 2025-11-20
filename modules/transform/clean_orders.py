import pandas as pd

def clean_orders(o50, h50):
    o50["source"] = "o50k"
    h50["source"] = "h50k"

    df = pd.concat([o50, h50], ignore_index=True)
    df = df.sort_values("modified_date").drop_duplicates("id", keep="last")
    df = df.sort_values("createdate").reset_index(drop=True)

    df["is_shipped"] = df["shipped"].notna()
    df = df.drop(columns=["externalid"], errors="ignore")

    return df
