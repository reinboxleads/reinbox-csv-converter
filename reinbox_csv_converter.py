import streamlit as st
import pandas as pd
from io import StringIO

# App branding and layout
st.set_page_config(page_title="REInbox Leads CSV Converter", page_icon="📬", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>📬 REInbox Leads CSV Converter</h1>
    <p style='text-align: center;'>This tool will clean and format your DealMachine export so it's ready for <strong>cold email campaigns in Instantly.</strong></p>
    <hr>
""", unsafe_allow_html=True)

st.markdown("""
### ✅ What This Tool Does:

- Splits each contact into **one row per email address**
- Duplicates all other contact info (owner name, property address, etc.)
- **Removes** anyone marked <code>"Resident, Likely Renting"</code>

---

### 🎯 What to Do:

1. Download your DealMachine contacts as a **CSV**
2. Paste the file directly into this converter
3. The cleaned version will download automatically
4. Then upload it straight into your **Instantly campaign**

---

⚠️ **Make sure your file includes the headers:** <code>email_address_1</code>, <code>email_address_2</code>, <code>email_address_3</code>
""", unsafe_allow_html=True)

# File upload
uploaded_file = st.file_uploader("Upload your DealMachine CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Normalize column headers (remove spaces, make lowercase)
        df.columns = df.columns.str.strip().str.lower()

        # Check for required email columns
        required_cols = ['email_address_1', 'email_address_2', 'email_address_3']
        if not all(col in df.columns for col in required_cols):
            st.error("⚠️ One or more email columns (email_address_1, _2, _3) are missing. Please check your headers.")
        else:
            # Remove contacts with "Resident, Likely Renting"
            if 'owner_first_name' in df.columns:
                df = df[df['owner_first_name'].str.strip().str.lower() != 'resident, likely renting']

            # Create rows for each available email
            rows = []
            for _, row in df.iterrows():
                for col in required_cols:
                    email = row[col]
                    if pd.notna(email) and email.strip() != "":
                        new_row = row.copy()
                        new_row['email_address'] = email.strip()
                        rows.append(new_row)

            if rows:
                result_df = pd.DataFrame(rows)
                # Drop original email_1, 2, 3 columns
                result_df = result_df.drop(columns=required_cols)

                # Create CSV for download
                csv = result_df.to_csv(index=False)
                st.success("✅ File cleaned and ready to download!")
                st.download_button(
                    label="📥 Download Clean CSV",
                    data=csv,
                    file_name="cleaned_dealmachine_leads.csv",
                    mime="text/csv"
                )
            else:
                st.warning("⚠️ No valid email addresses found to convert.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("☝️ Upload a .csv file above to get started.")
