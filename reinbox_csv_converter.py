import streamlit as st
import pandas as pd
from io import StringIO
import base64

st.set_page_config(page_title="REInbox Leads CSV Converter", page_icon="📬")

# Branding and Instructions
st.markdown("""
# 📬 REInbox Leads CSV Converter

This tool will clean and format your DealMachine export so it's ready for **cold email campaigns in Instantly**.

---

### ✅ What This Tool Does:
- Splits each contact into **one row per email address**
- Duplicates all other contact info (owner name, property address, etc.)
- **Removes** anyone marked `"Resident, Likely Renting"`

---

### 🧭 What to Do:
1. Download your DealMachine contacts as a **CSV**
2. Paste the file directly into this converter
3. The cleaned version will download automatically
4. Then upload it straight into your **Instantly campaign**

---

⚠️ **Make sure your file includes the headers:**
`email_address_1`, `email_address_2`, `email_address_3`

---
""")

# File upload
uploaded_file = st.file_uploader("Upload your DealMachine CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Check for required email columns
    required_cols = ['email_address_1', 'email_address_2', 'email_address_3']
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        st.warning(f"⚠️ Missing columns: {', '.join(missing_cols)}. Please check your file headers.")
    else:
        # Remove 'Resident, Likely Renting'
        df = df[df['owner_first_name'].str.strip().str.lower() != 'resident, likely renting']

        # Create one row per email address
        expanded_rows = []
        for _, row in df.iterrows():
            for email_col in required_cols:
                email = row[email_col]
                if pd.notnull(email) and str(email).strip() != '':
                    new_row = row.copy()
                    new_row['email_address'] = email
                    expanded_rows.append(new_row)

        if expanded_rows:
            cleaned_df = pd.DataFrame(expanded_rows)
            cleaned_df = cleaned_df.drop(columns=required_cols)

            # Generate CSV download
            csv = cleaned_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="REInbox_Cleaned_Leads.csv">📥 Download Cleaned CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("✅ Your cleaned file is ready!")
        else:
            st.warning("No valid emails found to process.")
else:
    st.info("☝️ Upload a .csv file above to get started.")
