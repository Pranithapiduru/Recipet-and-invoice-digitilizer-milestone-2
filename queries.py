from database.db import get_db


# ================= SAVE RECEIPT =================
def save_receipt(data):
    """
    Save receipt to database.
    Assumes data = {
        bill_id, vendor, date, amount, tax
    }
    """
    db = get_db()

    db.execute(
        """
        INSERT INTO receipts (bill_id, vendor, date, amount, tax)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["bill_id"],
            data["vendor"],
            data["date"],
            float(data["amount"]),
            float(data["tax"]),
        ),
    )
    db.commit()


# ================= DUPLICATE CHECK =================
def receipt_exists(bill_id):
    db = get_db()
    cur = db.execute(
        "SELECT 1 FROM receipts WHERE bill_id = ?",
        (bill_id,)
    )
    return cur.fetchone() is not None


# ================= FETCH ALL RECEIPTS =================
def fetch_all_receipts():
    """
    Returns list of dicts:
    [
      {bill_id, vendor, date, amount, tax},
      ...
    ]
    """
    db = get_db()
    cur = db.execute(
        "SELECT bill_id, vendor, date, amount, tax FROM receipts ORDER BY date DESC"
    )

    rows = cur.fetchall()

    return [
        {
            "bill_id": r["bill_id"],
            "vendor": r["vendor"],
            "date": r["date"],
            "amount": float(r["amount"]),
            "tax": float(r["tax"]),
        }
        for r in rows
    ]


# ================= DELETE ONE RECEIPT =================
def delete_receipt(bill_id):
    db = get_db()
    db.execute(
        "DELETE FROM receipts WHERE bill_id = ?",
        (bill_id,)
    )
    db.commit()


# ================= CLEAR ALL RECEIPTS =================
def clear_all_receipts():
    db = get_db()
    db.execute("DELETE FROM receipts")
    db.commit()
