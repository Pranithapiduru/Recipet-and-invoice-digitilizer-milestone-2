import streamlit as st


def render_sidebar():
    """
    Renders the application sidebar and
    returns the selected navigation page.
    """

    with st.sidebar:
        st.title("📁 Receipt Vault")

        # ================= GEMINI API =================
        st.subheader("🤖 Gemini AI")

        api_key = st.text_input(
            "Enter Gemini API Key",
            type="password",
            value=st.session_state.get("GEMINI_API_KEY", "")
        )

        if api_key:
            st.session_state.GEMINI_API_KEY = api_key
            st.success("✅ Gemini API Enabled")
        else:
            st.warning("⚠ Gemini API Not Set")

        st.divider()

        # ================= NAVIGATION =================
        page = st.radio(
            "Navigation",
            [
                "Upload Receipt",
                "Validation",
                "Analytics Dashboard"
            ],
            label_visibility="visible"
        )

        return page
