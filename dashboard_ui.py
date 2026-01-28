import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database.queries import (
    fetch_all_receipts,
    delete_receipt,
    clear_all_receipts
)


def dashboard_ui():
    st.header("📊 Analytics Dashboard")

    receipts = fetch_all_receipts()
    if not receipts:
        st.info("No receipts stored yet")
        return

    df = pd.DataFrame(receipts)

    # ================= METRICS =================
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Bills", len(df))
    m2.metric("Total Amount (₹)", f"{df['amount'].sum():.2f}")
    m3.metric("Total Tax (₹)", f"{df['tax'].sum():.2f}")
    m4.metric("Total Vendors", df["vendor"].nunique())

    st.divider()

    # ================= SEARCH =================
    st.subheader("🔍 Search Stored Receipts")
    s1, s2, s3, s4 = st.columns(4)

    bill_id = s1.text_input("Bill ID")
    vendor = s2.text_input("Vendor")
    amount = s3.text_input("Amount")
    tax = s4.text_input("Tax")

    filtered = df.copy()

    if bill_id:
        filtered = filtered[filtered["bill_id"].str.contains(bill_id, case=False)]
    if vendor:
        filtered = filtered[filtered["vendor"].str.contains(vendor, case=False)]
    if amount:
        try:
            filtered = filtered[filtered["amount"] == float(amount)]
        except ValueError:
            pass
    if tax:
        try:
            filtered = filtered[filtered["tax"] == float(tax)]
        except ValueError:
            pass

    st.divider()

    # ================= STORED RECEIPTS (REAL TABLE) =================
    st.subheader("📁 Stored Receipts")

    display_df = filtered.rename(columns={
        "bill_id": "Bill ID",
        "vendor": "Vendor",
        "date": "Date",
        "amount": "Amount (₹)",
        "tax": "Tax (₹)"
    })

    st.dataframe(
        display_df,
        use_container_width=True,
        height=350
    )

    # ================= DELETE SECTION =================
    st.subheader("🗑️ Delete Receipt")

    delete_bill = st.selectbox(
        "Select Bill ID to delete",
        options=filtered["bill_id"].tolist()
    )

    if st.button("Delete Selected Bill"):
        delete_receipt(delete_bill)
        st.success(f"Deleted bill {delete_bill}")
        st.rerun()

    st.divider()

    # ================= CLEAR ALL =================
    if st.button("🧹 Clear All Bills"):
        clear_all_receipts()
        st.success("All receipts cleared")
        st.rerun()

    st.divider()

    # ================= ANALYTICS =================
    st.subheader("📈 Analytics Overview")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    vendor_amount = (
        df.groupby("vendor")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    timeline = (
        df.groupby("date")["amount"]
        .sum()
        .sort_index()
    )

    c1, c2 = st.columns(2)

    # ---- PIE CHART ----
    with c1:
        st.markdown("**Vendor-wise Spend**")
        fig1, ax1 = plt.subplots(figsize=(4, 4))
        ax1.pie(
            vendor_amount,
            labels=vendor_amount.index,
            autopct="%1.1f%%",
            startangle=90,
            textprops={"fontsize": 9}
        )
        ax1.axis("equal")
        st.pyplot(fig1)

    # ---- BAR CHART ----
    with c2:
        st.markdown("**Vendor vs Amount**")
        st.bar_chart(vendor_amount, height=260)

    st.divider()

    # ---- TIMELINE ----
    st.markdown("**📅 Spending Timeline**")
    st.line_chart(timeline, height=260)
