import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Bathing Water Quality Explorer", layout="wide")

st.title("🌊 Bathing Water Quality Explorer")
st.markdown("""
This tool helps the Environment Agency and partners explore relationships between bathing water quality indicators (e.g. E. coli) and environmental factors such as rainfall, tides, and effluent discharge. Upload your dataset to get started.
""")

# File uploader
uploaded_file = st.file_uploader("Upload your data file (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            df = pd.read_csv(uploaded_file)

        st.success("File uploaded successfully!")

        st.subheader("Raw Data Preview")
        st.dataframe(df.head(50))

        # Convert all numeric columns
        for col in df.select_dtypes(include='object').columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')

        numeric_columns = filtered_df.select_dtypes(include='number').columns.tolist()
        x_var = st.selectbox("Select X-axis variable", numeric_columns)
        y_var = st.selectbox("Select Y-axis variable", numeric_columns, index=1 if len(numeric_columns) > 1 else 0)

        st.subheader("📈 Correlation Plot")
        fig, ax = plt.subplots()
        sns.regplot(data=filtered_df, x=x_var, y=y_var, ax=ax, line_kws={'color': 'red'})
        ax.set_title(f"Correlation between {x_var} and {y_var}")
        st.pyplot(fig)

        st.subheader("📊 Correlation Matrix")
        corr_matrix = filtered_df[numeric_columns].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        st.subheader("📉 Line Graph: Overlapping Variables")
        selected_lines = st.multiselect("Select multiple variables to overlay on a line chart", numeric_columns, default=numeric_columns[:2])
        if len(selected_lines) > 1:
            st.line_chart(filtered_df[selected_lines].dropna())

        st.subheader("📊 Summary Statistics")
        st.write(filtered_df[[x_var, y_var]].describe())

        st.download_button("Download filtered data as CSV", filtered_df.to_csv(index=False), file_name=f"filtered_data_{selected_site}.csv")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a dataset to begin.")
