import pandas as pd


def split_train_test_data(
    data: pd.DataFrame, train_pct: float = 0.7
) -> tuple[pd.DataFrame, pd.DataFrame]:
    idx = int(data.shape[0] * train_pct)
    dates = data.index.values
    train = dates[:idx]

    train_df = data[data.index.isin(train)]
    test_df = data[~data.index.isin(train)]

    return train_df, test_df
