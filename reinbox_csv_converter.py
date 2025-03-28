import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="REInbox CSV Converter", layout="centered")
st.title("📬 REInbox Leads CSV Converter")
st.markdown("This tool will clean and format your DealMachine export by splitting emails and removing 'Resident, Likely Renting' contacts.")

uploaded_file = st.file_uploader("Upload your DealMachine CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Try to find the column that includes "Resident, Likely Renting"
    owner_col = None
    for col in df.columns:
        if df[col].astype(str).str.contains("Resident, Likely Renting", case=False).any():
            owner_col = col
            break

    if owner_col:
        df = df[~df[owner_col].astype(str).str.contains("Resident, Likely Renting", case=False, na=False)]

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
        st.success("✅ File processed successfully!")

        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv,
            file_name="reibox-cleaned-leads.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ No valid emails found to process.")
