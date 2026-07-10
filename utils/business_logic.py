from datetime import datetime


def enrich_invoice(invoice):

    today = datetime.today()

    # ------------------------------------
    # Calculate Aging
    # ------------------------------------

    try:

        invoice_date = datetime.strptime(
            invoice["invoice_date"],
            "%d %b %Y"
        )

        days = (today - invoice_date).days

    except:

        days = 0

    if days <= 7:

        bucket = "0-7"

    elif days <= 15:

        bucket = "8-15"

    elif days <= 30:

        bucket = "16-30"

    elif days <= 60:

        bucket = "31-60"

    else:

        bucket = "60+"

    # ------------------------------------
    # Dashboard Fields
    # ------------------------------------

    invoice["status"] = "Pending"

    invoice["approval"] = "Pending"

    invoice["duplicate"] = False

    invoice["exception"] = False

    invoice["payment_delay"] = False

    invoice["compliance_issue"] = False

    invoice["days"] = days

    invoice["aging_bucket"] = bucket

    return invoice