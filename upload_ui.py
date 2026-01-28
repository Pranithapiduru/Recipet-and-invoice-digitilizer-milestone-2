import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd

from ocr.text_parser import parse_receipt
from ui.validation_ui import validate_receipt
from database.queries import save_receipt, receipt_exists


def render_upload_ui():
    st.header("📤 Upload Receipt")

    uploaded = st.file_uploader(
        "Upload receipt image",
        type=["png", "jpg", "jpeg"]
    )

    if not uploaded:
        st.info("Please upload a receipt image to begin")
        return

    # ================= IMAGE PREVIEW =================
    img = Image.open(uploaded)

    col1, col2 = st.columns(2)
    with col1:
        st.image(img, caption="Original Image", use_container_width=True)

    with col2:
        gray = img.convert("L")
        st.image(gray, caption="Processed Image", use_container_width=True)

    st.divider()

    # ================= OCR + PARSE =================
    if not st.button("📄 Extract & Save Receipt", use_container_width=True):
        return

    with st.spinner("Extracting text from receipt..."):
        text = pytesseract.image_to_string(gray)

    if not text.strip():
        st.error("❌ No readable text detected from the image")
        return

    # NLP parsing
    data, items = parse_receipt(text)

    st.session_state["LAST_EXTRACTED_RECEIPT"] = data

    # ================= RECEIPT SUMMARY (HORIZONTAL TABLE) =================
    st.subheader("🧾 Receipt Summary")

    summary_df = pd.DataFrame([{
        "Bill ID": data["bill_id"],
        "Vendor": data["vendor"],
        "Date": data["date"],
        "Amount (₹)": round(data["amount"], 2),
        "Tax (₹)": round(data["tax"], 2),
    }])

    st.dataframe(summary_df, use_container_width=True)

    # ================= ITEM WISE EXTRACTION =================
    st.subheader("🛒 Item-wise Details")

    if items and len(items) > 0:
        st.dataframe(items, use_container_width=True)
    else:
        st.info("No item-wise details detected from this receipt")

    st.divider()

    # ================= DUPLICATE CHECK =================
    if receipt_exists(data["bill_id"]):
        st.error("❌ Duplicate detected — receipt NOT saved to database")
        return
    else:
        st.success("✅ No duplicate found")

    # ================= VALIDATION =================
    validation = validate_receipt(data)
    st.session_state["LAST_VALIDATION_REPORT"] = validation

    # ================= SAVE (EVEN IF VALIDATION FAILS) =================
    save_receipt(data)

    if validation["passed"]:
        st.success("🎉 Receipt passed validation and was saved successfully")
    else:
        st.error("❌ Receipt failed validation")
