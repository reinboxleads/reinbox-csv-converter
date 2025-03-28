import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="REInbox Leads CSV Converter", page_icon="📬", layout="centered")

st.markdown("<h1 style='text-align: center;'>📬 REInbox Leads CSV Converter</h1>", unsafe_allow_html=True)
st.write("This tool will clean and format your DealMachine export by splitting emails and removing 'Resident, Likely Renting' contacts.")

uploaded_file = st.file_uploader("Upload your DealMachine CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Check required columns
    required_columns = ["email_address_1", "email_address_2", "email_address_3", "owner_name"]
    if not all(col in df.columns for col in required_columns):
        st.warning("⚠️ One or more email columns (email_address_1, _2, _3) or owner_name are missing. Please check your headers.")
    else:
        # Remove rows with 'Resident, Likely Renting'
        df = df[df['owner_name'].str.strip().str.lower() != 'resident, likely renting']

        expanded_rows = []
        for _, row in df.iterrows():
            for col in ["email_address_1", "email_address_2", "email_address_3"]:
                email = row[col]
                if pd.notnull(email) and email.strip() != "":
                    new_row = row.copy()
                    new_row["email"] = email
                    expanded_rows.append(new_row)

        if expanded_rows:
            new_df = pd.DataFrame(expanded_rows)
            new_df.drop(columns=["email_address_1", "email_address_2", "email_address_3"], inplace=True)

            csv = new_df.to_csv(index=False)
            st.success("✅ Done! Your file is ready to download.")
            st.download_button(label="📥 Download Clean CSV", data=csv, file_name="cleaned_dealmachine.csv", mime="text/csv")
        else:
            st.warning("⚠️ No valid email addresses found.")
