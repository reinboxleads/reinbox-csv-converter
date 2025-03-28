
import streamlit as st
import pandas as pd
import io

# Set page config with title and logo
st.set_page_config(
    page_title="REInbox Leads Converter",
    page_icon="📬",
    layout="centered"
)

# Header and instructions
st.title("📬 REInbox Leads Converter")
st.markdown("""
**Format your DealMachine CSV for cold email outreach—quickly and easily.**

- Removes “Resident, Likely Renting” contacts  
- Duplicates rows for each valid email address  
- Outputs a clean CSV for Instantly, Smartlead, or Mailshake  

⬆️ **Upload your DealMachine export above**  
⬇️ **Download your formatted cold email list below**
""")

uploaded_file = st.file_uploader("📂 Upload your DealMachine CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Remove "Resident, Likely Renting"
    owner_col = None
    for col in df.columns:
        if df[col].astype(str).str.contains("Resident, Likely Renting", case=False).any():
            owner_col = col
            break
    if owner_col:
        df = df[~df[owner_col].astype(str).str.contains("Resident, Likely Renting", case=False, na=False)]

    # Extract emails and duplicate rows
    email_cols = ['email_address_1', 'email_address_2', 'email_address_3']
    email_cols_present = [col for col in email_cols if col in df.columns]

    rows = []
    for _, row in df.iterrows():
        for email_col in email_cols_present:
            if pd.notna(row[email_col]) and row[email_col].strip():
                new_row = row.copy()
                new_row['email_address'] = row[email_col]
                rows.append(new_row)

    if rows:
        cleaned_df = pd.DataFrame(rows)
        cleaned_df.drop(columns=email_cols_present, inplace=True)
        csv = cleaned_df.to_csv(index=False).encode("utf-8")
        st.success("✅ File formatted and ready to go!")

        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv,
            file_name="reinbox-formatted-leads.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ No valid emails found to process.")
