import re

def extract_fields(text):
    fields = {}

    fields["date"] = re.search(r"\d{2}/\d{2}/\d{4}", text)
    fields["date"] = fields["date"].group() if fields["date"] else None

    fields["invoice"] = re.search(r"INV[-\d]+", text)
    fields["invoice"] = fields["invoice"].group() if fields["invoice"] else None

    fields["tax"] = re.search(r"TAX\s+([\d\.]+)", text)
    fields["tax"] = float(fields["tax"].group(1)) if fields["tax"] else 0.0

    return fields
