import sqlite3
from pathlib import Path

import pandas as pd

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------

DATA_PATH = Path("data/invoice_dataset.xlsx")
DATABASE_PATH = Path("data/invoice.db")

TABLE_NAME = "invoices"


# -------------------------------------------------------------------
# Load and Clean Excel
# -------------------------------------------------------------------

def load_excel() -> pd.DataFrame:
    """
    Load invoice dataset from Excel and perform basic cleaning.
    """

    df = pd.read_excel(DATA_PATH)

    # Convert dates
    date_columns = [
        "Invoice Date",
        "PO Date",
        "Email Received At"
    ]

    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Convert numeric columns
    numeric_columns = [
        "Invoice Amount",
        "Gross Amount",
        "Invoice Tax Amount",
        "Quantity",
        "Unit Cost",
        "Weight",
        "Amount in Invoice",
        "Received Quantity",
        "Gross Amount1",
        "Tax"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


# -------------------------------------------------------------------
# Create SQLite Database
# -------------------------------------------------------------------

def create_database():
    """
    Read Excel and store data into SQLite.
    """

    df = load_excel()

    conn = sqlite3.connect(DATABASE_PATH)

    df.to_sql(
        TABLE_NAME,
        conn,
        if_exists="replace",
        index=False
    )

    conn.commit()
    conn.close()

    print(f"Database created successfully.")
    print(f"Rows inserted : {len(df)}")


# -------------------------------------------------------------------
# Database Connection
# -------------------------------------------------------------------

def get_connection():

    return sqlite3.connect(DATABASE_PATH)


# -------------------------------------------------------------------
# Test Database
# -------------------------------------------------------------------

def test_database():

    conn = get_connection()

    df = pd.read_sql(
        f"SELECT * FROM {TABLE_NAME} LIMIT 5",
        conn
    )

    conn.close()

    print(df)


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

if __name__ == "__main__":

    create_database()

    test_database()