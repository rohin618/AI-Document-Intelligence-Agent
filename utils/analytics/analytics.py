import pandas as pd
import numpy as np

from utils.database.database import get_connection


def load_invoice_data():

    conn = get_connection()

    df = pd.read_sql("SELECT * FROM invoices", conn)

    conn.close()

    return df


def get_dashboard_summary(df):

    duplicates = df.duplicated(subset=["Invoice No"], keep=False).sum()


    return {
        "totalInvoices": len(df),
        "totalPOs": df["PO Number"].nunique(),
        "totalVendors": df["Vendor Name"].nunique(),
        "totalSpend": round(float(df["Invoice Amount"].sum()), 2),
        "averageInvoice": round(float(np.mean(df["Invoice Amount"])), 2),
        "highestInvoice": round(float(np.max(df["Invoice Amount"])), 2),
        "lowestInvoice": round(float(np.min(df["Invoice Amount"])), 2),
        "duplicateInvoices": int(duplicates),
    }


def get_vendor_ranking(df):

    vendors = (
        df.groupby("Vendor Name")["Invoice Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    return [
        {"vendor": vendor, "amount": round(float(amount), 2)}
        for vendor, amount in vendors.items()
    ]


def get_category_analysis(df):

    categories = (
        df.groupby("Category")["Invoice Amount"].sum().sort_values(ascending=False)
    )

    return [
        {"category": category, "amount": round(float(amount), 2)}
        for category, amount in categories.items()
    ]


def get_monthly_spend(df):

    df = df.copy()

    df["Invoice Date"] = pd.to_datetime(df["Invoice Date"], errors="coerce")

    df = df.dropna(subset=["Invoice Date"])

    monthly = (
        df.groupby(df["Invoice Date"].dt.strftime("%Y-%m"))["Invoice Amount"]
        .sum()
        .sort_index()
    )

    return [
        {"month": month, "amount": round(float(amount), 2)}
        for month, amount in monthly.items()
    ]


def get_matched_status(df):

    status = df["Matched Status"].value_counts()

    return [{"status": s, "count": int(c)} for s, c in status.items()]


def get_received_status(df):

    status = df["Received Status"].value_counts()

    return [{"status": s, "count": int(c)} for s, c in status.items()]


def get_numpy_statistics(df):

    amounts = df["Invoice Amount"].to_numpy()

    return {
        "mean": round(float(np.mean(amounts)), 2),
        "median": round(float(np.median(amounts)), 2),
        "std": round(float(np.std(amounts)), 2),
        "variance": round(float(np.var(amounts)), 2),
        "minimum": round(float(np.min(amounts)), 2),
        "maximum": round(float(np.max(amounts)), 2),
        "percentile95": round(float(np.percentile(amounts, 95)), 2),
    }


def get_dashboard_data():

    df = load_invoice_data()

    return {
        "summary": get_dashboard_summary(df),
        "vendors": get_vendor_ranking(df),
        "categories": get_category_analysis(df),
        "monthlySpend": get_monthly_spend(df),
        "matchedStatus": get_matched_status(df),
        "receivedStatus": get_received_status(df),
        "statistics": get_numpy_statistics(df),
        "recentInvoices": get_recent_invoices(df),
        "buyers": get_top_buyers(df),
        "vendorInvoiceCount": get_vendor_invoice_count(df),
        "matchingPercentage": get_matching_percentage(df),
        "categoryCount": get_category_count(df),
    }


def get_recent_invoices(df):

    df = df.copy()

    df["Invoice Date"] = pd.to_datetime(df["Invoice Date"], errors="coerce")

    recent = df.sort_values("Invoice Date", ascending=False).head(10)

    return [
        {
            "invoiceNo": row["Invoice No"],
            "vendor": row["Vendor Name"],
            "category": row["Category"],
            "amount": round(float(row["Invoice Amount"]), 2),
            "status": row["Matched Status"],
            "date": str(row["Invoice Date"])[:10],
        }
        for _, row in recent.iterrows()
    ]


def get_top_buyers(df):

    buyers = (
        df.groupby("Buyer Name")["Invoice Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    return [
        {"buyer": buyer, "amount": round(float(amount), 2)}
        for buyer, amount in buyers.items()
    ]


def get_vendor_invoice_count(df):

    counts = df["Vendor Name"].value_counts().head(10)

    return [{"vendor": vendor, "count": int(count)} for vendor, count in counts.items()]


def get_matching_percentage(df):

    total = len(df)

    matched = (df["Matched Status"] == "Matched").sum()

    partial = (df["Matched Status"] == "Partial Match").sum()

    duplicate = (df["Matched Status"] == "Duplicates").sum()

    return {
        "matched": round(matched / total * 100, 2),
        "partial": round(partial / total * 100, 2),
        "duplicates": round(duplicate / total * 100, 2),
    }


def get_category_count(df):

    counts = df["Category"].value_counts().head(10)

    return [
        {"category": category, "count": int(count)}
        for category, count in counts.items()
    ]


if __name__ == "__main__":

    data = get_dashboard_data()

    from pprint import pprint

    pprint(data)
