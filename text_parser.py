import re
from datetime import datetime
import random


# ---------- HELPERS ----------

def _clean_amount(val):
    try:
        return float(val.replace(",", ""))
    except Exception:
        return 0.0


def _default_bill_id():
    return f"BILL-{random.randint(100000, 999999)}"


def _extract_date(text):
    """
    NLP-style date extraction (multiple formats)
    """
    patterns = [
        r"\b(\d{4}-\d{2}-\d{2})\b",          # 2024-01-27
        r"\b(\d{2}/\d{2}/\d{4})\b",          # 27/01/2024
        r"\b(\d{2}-\d{2}-\d{4})\b",          # 27-01-2024
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            raw = m.group(1)
            try:
                if "-" in raw and raw.count("-") == 2:
                    return datetime.strptime(raw, "%Y-%m-%d").strftime("%Y-%m-%d")
                if "/" in raw:
                    return datetime.strptime(raw, "%d/%m/%Y").strftime("%Y-%m-%d")
            except Exception:
                pass

    # fallback → today
    return datetime.today().strftime("%Y-%m-%d")


# ---------- MAIN PARSER ----------

def parse_receipt(text: str):
    """
    RETURNS:
    data  -> dict
    items -> list of dicts
    """

    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # ---------- BILL ID ----------
    bill_id = None
    for l in lines:
        if re.search(r"(bill|invoice|receipt)\s*[:#]?\s*(\w+)", l, re.I):
            bill_id = re.findall(r"\w+", l)[-1]
            break

    if not bill_id:
        bill_id = _default_bill_id()

    # ---------- VENDOR ----------
    vendor = lines[0] if lines else "Unknown Vendor"

    # ---------- DATE ----------
    date = _extract_date(text)

    # ---------- TOTAL ----------
    total = 0.0
    tax = 0.0

    for l in lines:
        if re.search(r"\btotal\b", l, re.I):
            nums = re.findall(r"\d+[.,]?\d*", l)
            if nums:
                total = _clean_amount(nums[-1])

        if re.search(r"\b(tax|gst|vat)\b", l, re.I):
            nums = re.findall(r"\d+[.,]?\d*", l)
            if nums:
                tax = _clean_amount(nums[-1])

    if tax > total:
        tax = 0.0

    if total == 0.0:
        # fallback: max numeric value
        nums = re.findall(r"\d+[.,]?\d*", text)
        if nums:
            total = max(_clean_amount(n) for n in nums)

    # ---------- ITEMS (NLP-ish heuristic) ----------
    items = []

    for l in lines:
        if re.search(r"\d+\s*x\s*\d+", l):
            continue

        m = re.match(r"(.+?)\s+(\d+[.,]?\d*)$", l)
        if m:
            name = m.group(1)
            price = _clean_amount(m.group(2))

            if 0 < price < total:
                items.append({
                    "Item": name,
                    "Price": price
                })

    # ---------- FINAL DATA ----------
    data = {
        "bill_id": bill_id,
        "vendor": vendor,
        "date": date,
        "amount": round(total, 2),
        "tax": round(tax, 2)
    }

    return data, items
