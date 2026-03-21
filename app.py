import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(page_title="MalobaAl Clean", layout="wide")

# Title
st.title("🧹 MalobaAl Clean")
st.write("Smart Data Cleaning for Africa")

# Upload file
uploaded_file = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])

if uploaded_file is not None:

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Data preview
    st.subheader("📊 Data Preview")
    st.dataframe(df)

    # Data info
    st.subheader("📌 Data Info")
    st.write("Rows & Columns:", df.shape)
    st.write("Missing Values:")
    st.write(df.isnull().sum())

    # ------------------------
    # One-Click Auto Clean
    # ------------------------
    st.subheader("⚡ One-Click Auto Clean")

    if st.button("Run Auto Clean"):
        # 1️⃣ Remove duplicates
        df = df.drop_duplicates()

        # 2️⃣ Fill missing values with 0
        df = df.fillna(0)

        # 3️⃣ Phone standardization
        if 'Phone' in df.columns:
            def standardize_phone(number):
                if pd.isna(number):
                    return number
                num = str(number)
                if num.startswith("0"):
                    return "+255" + num[1:]
                elif num.startswith("255"):
                    return "+" + num
                elif num.startswith("+255"):
                    return num
                else:
                    return num
            df['Phone_Standardized'] = df['Phone'].apply(standardize_phone)

        # 4️⃣ Date standardization
        if 'Date Joined' in df.columns:
            df['Date_Standardized'] = pd.to_datetime(df['Date Joined'], errors='coerce', dayfirst=True)

        # 5️⃣ Name duplicate detection (case insensitive)
        if 'Name' in df.columns:
            df['Name_lower'] = df['Name'].str.lower()
            duplicates = df[df.duplicated('Name_lower', keep=False)]
            if not duplicates.empty:
                st.warning(f"⚠ Found {duplicates.shape[0]} potential duplicate names")
            else:
                st.success("✅ No duplicate names found")

        st.success("✅ Auto Clean Completed")
        st.dataframe(df)

        # Download cleaned file
        st.download_button(
            label="⬇ Download Cleaned Data",
            data=df.to_csv(index=False),
            file_name="cleaned_data.csv",
            mime="text/csv"
        )