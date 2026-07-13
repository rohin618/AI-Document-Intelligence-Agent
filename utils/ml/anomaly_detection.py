from sklearn.ensemble import IsolationForest


def detect_anomalies(df):

    df = df.copy()

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    df["Prediction"] = model.fit_predict(
        df[["Invoice Amount"]]
    )

    df["Status"] = df["Prediction"].map({
        1: "Normal",
        -1: "Anomaly"
    })

    # Keep only anomalies
    anomalies = df[df["Status"] == "Anomaly"]

    # Top 10 highest anomalous invoices
    anomalies = (
        anomalies
        .sort_values("Invoice Amount", ascending=False)
        .head(10)
    )

    return {

        "labels": anomalies["Invoice No"].tolist(),

        "amounts": anomalies["Invoice Amount"].tolist(),

        "vendors": anomalies["Vendor Name"].tolist(),

        "count": len(anomalies)

    }