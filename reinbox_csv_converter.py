import streamlit as st
import pandas as pd

st.set_page_config(page_title="REInbox Leads CSV Converter", page_icon="📬", layout="centered")

st.markdown("<h1 style='text-align: center;'>📬 REInbox Leads CSV Converter</h1>", unsafe_allow_html=True)
st.write("This tool will clean and format your DealMachine export so it's ready for cold email campaigns in Instantly.")

st.markdown("---")
st.markdown("### ✅ What This Tool Does:")
st.markdown("""
- Removes anyone marked <span style='color: green; font-weight: bold'>"Resident, Likely Renting"</span>  
- Removes extra email columns (only keeps `email_address_1`)  
- Removes emails unlikely to be active  
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🎯 What to Do:")
st.markdown("""
1. **Download** your DealMachine contacts as a **CSV**  
2. **Paste** the file directly into this converter  
3. The cleaned version will download automatically  
4. Then upload it straight into your **Instantly** campaign  
""")

uploaded_file = st.file_uploader("📁 Upload your DealMachine CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Confirm required columns exist
    required_cols = ["email_address_1", "owner_name"]
    if not all(col in df.columns for col in required_cols):
        st.warning("⚠️ Missing 'email_address_1' or 'owner_name'. Please check your CSV headers.")
    else:
        # Filter out renters
        df = df[df["owner_name"].str.strip().str.lower() != "resident, likely renting"]

        # Remove rows with missing/invalid email_address_1
        df = df[df["email_address_1"].notnull()]
        df = df[df["email_address_1"].str.strip() != ""]

        # Drop email_address_2 and email_address_3 if they exist
        for col in ["email_address_2", "email_address_3"]:
            if col in df.columns:
                df.drop(columns=col, inplace=True)

        # Final output
        if len(df) > 0:
            cleaned_csv = df.to_csv(index=False)
            st.success("✅ Done! Your cleaned file is ready to download.")
            st.download_button("📥 Download Clean CSV", cleaned_csv, file_name="cleaned_dealmachine.csv", mime="text/csv")
        else:
            st.warning("⚠️ No valid leads found after cleaning.")
