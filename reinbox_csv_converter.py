import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="REInbox Leads CSV Converter", page_icon="📬", layout="centered")

st.markdown("<h1 style='text-align: center;'>📬 REInbox Leads CSV Converter</h1>", unsafe_allow_html=True)
st.write("""
This tool cleans and formats your DealMachine lead list for cold email campaigns:

✅ Removes renters (contacts marked "Resident, Likely Renting")  
✅ Removes unused or unlikely-to-be-active emails  
""")

uploaded_file = st.file_uploader("Upload your DealMachine CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Confirm required columns exist
    required_columns = ["email_address_1", "email_address_2", "email_address_3", "contact_flags"]
    if not all(col in df.columns for col in required_columns):
        st.warning("⚠️ Your file is missing one or more required columns. Please check your export.")
    else:
        # Remove 'Resident, Likely Renting'
        df = df[~df["contact_flags"].str.strip().str.lower().eq("resident, likely renting")]

        # Drop secondary email columns
        df.drop(columns=["email_address_2", "email_address_3"], inplace=True)

        # Remove contacts with no primary email
        df = df[df["email_address_1"].notna() & (df["email_address_1"].str.strip() != "")]

        # Save cleaned CSV
        cleaned_csv = df.to_csv(index=False)
        st.success("✅ Done! Your file is ready to download.")
        st.download_button(
            label="📥 Download Clean CSV",
            data=cleaned_csv,
            file_name="cleaned_dealmachine.csv",
            mime="text/csv"
        )
