import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def predict_monthly_spend(df):
    """
    Predict next month's spend using Linear Regression.

    Returns chart-ready data.
    """

    df = df.copy()

    df["Invoice Date"] = pd.to_datetime(
        df["Invoice Date"],
        errors="coerce"
    )

    df = df.dropna(subset=["Invoice Date"])

    monthly = (
        df.groupby(df["Invoice Date"].dt.to_period("M"))["Invoice Amount"]
        .sum()
        .reset_index()
    )

    monthly["Month"] = monthly["Invoice Date"].astype(str)

    monthly["MonthIndex"] = np.arange(len(monthly))

    X = monthly[["MonthIndex"]]
    y = monthly["Invoice Amount"]

    model = LinearRegression()

    model.fit(X, y)

    next_index = len(monthly)

    prediction = model.predict(
    pd.DataFrame(
        {"MonthIndex": [next_index]}
    )
    )[0]

    next_month = (
        monthly.iloc[-1]["Invoice Date"] + 1
    )

    labels = monthly["Month"].tolist()
    labels.append(str(next_month))

    actual = monthly["Invoice Amount"].tolist()
    actual.append(None)

    predicted = [None] * len(monthly)
    predicted.append(round(float(prediction), 2))

    return {
        "labels": labels,
        "actual": actual,
        "predicted": predicted,
        "predictedSpend": round(float(prediction), 2)
    }