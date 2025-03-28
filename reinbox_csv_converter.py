import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="REInbox Leads CSV Converter", layout="centered")

st.markdown("""
    <h1>📬 REInbox Leads CSV Converter</h1>
    <p>This tool will clean and format your DealMachine export so it's ready for <strong>cold email campaigns in Instantly</strong>.</p>
    <hr>
""", unsafe_allow_html=True)

st.markdown("""
### ✅ What This Tool Does:

- Splits each contact into <strong>one row per email address</strong>
- Duplicates all other contact info (owner name, property address, etc.)
- <strong>Removes anyone marked</strong> <code>"Resident, Likely Renting"</code>
""", unsafe_allow_html=True)

st.markdown("""---""")

st.markdown("""
### 🎯 What to Do:

1. Download your DealMachine contacts as a <strong>CSV</strong>  
2. Paste the file directly into this converter  
3. The cleaned version will download automatically  
4. Then upload it straight into your <strong>Instantly campaign</strong>
""", unsafe_allow_html=True)

st.markdown("""
⚠️ <strong>Make sure your file includes the headers:</strong> <code>email_address_1</code>, <code>email_address_2</code>, <code>email_address_3</code>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your DealMachine CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    email_columns = ['email_address_1', 'email_address_2', 'email_address_3']
    if not all(col in df.columns for col in email_columns):
        st.error("⚠️ One or more email columns (email_address_1, _2, _3) are missing. Please check your headers.")
    else:
        # Remove "Resident, Likely Renting" from contact_flags
        if 'contact_flags' in df.columns:
            df = df[~df['contact_flags'].fillna('').str.strip().str.lower().eq('resident, likely renting')]

        expanded_rows = []
        for _, row in df.iterrows():
            for col in email_columns:
                email = str(row[col]).strip()
                if email and email.lower() != 'nan':
                    new_row = row.copy()
                    new_row['email'] = email
                    expanded_rows.append(new_row)

        if expanded_rows:
            final_df = pd.DataFrame(expanded_rows)
            final_df.drop(columns=email_columns, inplace=True, errors='ignore')

            # Prepare download
            buffer = BytesIO()
            final_df.to_csv(buffer, index=False)
            buffer.seek(0)
            st.success("✅ Conversion complete. Your file is ready to download.")
            st.download_button(
                label="📥 Download Cleaned CSV",
                data=buffer,
                file_name="cleaned_reinbox_leads.csv",
                mime="text/csv"
            )
        else:
            st.warning("No valid emails found to convert.")
else:
    st.info("☝️ Upload a .csv file above to get started.")
