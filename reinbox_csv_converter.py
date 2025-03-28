import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="REInbox Leads CSV Converter", page_icon="📬", layout="centered")

st.markdown(
    "<h1 style='text-align: center;'>📬 REInbox Leads CSV Converter</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>This tool will clean and format your DealMachine export by splitting emails and removing 'Resident, Likely Renting' contacts.</p>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload your DealMachine CSV file", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Make column headers lowercase for easier handling
        df.columns = [col.lower() for col in df.columns]

        # Check for required email columns
        required_cols = ["email_address_1", "email_address_2", "email_address_3"]
        if not all(col in df.columns for col in required_cols):
            st.warning("⚠️ One or more email columns (email_address_1, _2, _3) are missing. Please check your headers.")
        else:
            # Remove rows where the name contains "Resident, Likely Renting"
            df = df[~df["owner_first_name"].str.contains("Resident, Likely Renting", case=False, na=False)]

            # Explode email columns into separate rows
            expanded_rows = []
            for _, row in df.iterrows():
                for email_col in required_cols:
                    email = row[email_col]
                    if pd.notna(email) and email.strip() != "":
                        new_row = row.copy()
                        new_row["email"] = email
                        expanded_rows.append(new_row)

            if not expanded_rows:
                st.warning("⚠️ No valid email addresses found.")
            else:
                result_df = pd.DataFrame(expanded_rows)
                result_df = result_df.drop(columns=required_cols)

                csv = result_df.to_csv(index=False).encode("utf-8")
                st.success("✅ Your file is ready!")
                st.download_button(
                    label="📥 Download Clean CSV",
                    data=csv,
                    file_name="cleaned_dealmachine_export.csv",
                    mime="text/csv"
                )
    except Exception as e:
        st.error(f"Something went wrong: {e}")
else:
    st.info("👆 Upload a .csv file above to get started.")
