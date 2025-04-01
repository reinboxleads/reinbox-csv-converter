import streamlit as st
import pandas as pd

st.set_page_config(page_title="REInbox Leads CSV Converter", page_icon="📬", layout="centered")

st.markdown("<h1 style='text-align: center;'>📬 REInbox Leads CSV Converter</h1>", unsafe_allow_html=True)
st.write("This tool will clean and format your DealMachine export so it's ready for cold email campaigns in Instantly.")

st.markdown("### ✅ What This Tool Does:")
st.markdown("""
- Removes **Resident, Likely Renting**
- Keeps only the **primary email field** (`email_address_1`)
- Removes obviously inactive emails like `@example.com`
""")

st.markdown("### 🎯 What to Do:")
st.markdown("""
1. Download your DealMachine contacts as a **CSV**
2. Paste the file directly into this converter
3. The cleaned version will download automatically
4. Upload it straight into your **Instantly campaign**

⚠️ Make sure your file includes the headers: `email_address_1`, `owner_name`
""")

uploaded_file = st.file_uploader("📤 Upload your DealMachine CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Check required columns
    required_columns = ["email_address_1", "owner_name"]
    if not all(col in df.columns for col in required_columns):
        st.warning("⚠️ Missing 'email_address_1' or 'owner_name'. Please check your CSV headers.")
    else:
        # Remove "Resident, Likely Renting"
        df = df[df['owner_name'].str.strip().str.lower() != 'resident, likely renting']

        # Remove obviously inactive or placeholder emails
        def is_valid_email(email):
            if pd.isnull(email):
                return False
            email = email.strip().lower()
            return email and "@example.com" not in email and "test@" not in email and not email.startswith("noreply")

        df = df[df['email_address_1'].apply(is_valid_email)]

        # Drop email_address_2 and email_address_3 if they exist
        for col in ["email_address_2", "email_address_3"]:
            if col in df.columns:
                df.drop(columns=[col], inplace=True)

        # Download cleaned file
        csv = df.to_csv(index=False)
        st.success("✅ Done! Your file is ready to download.")
        st.download_button(label="📥 Download Clean CSV", data=csv, file_name="cleaned_dealmachine.csv", mime="text/csv")
