import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression


def train():
    df = pd.read_csv("sales_data.csv")

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    df["day_index"] = np.arange(len(df))

    X = df[["day_index"]]
    y = df["sales"]

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, "model.pkl")

    print("Model trained and saved.")


if __name__ == "__main__":
    train()