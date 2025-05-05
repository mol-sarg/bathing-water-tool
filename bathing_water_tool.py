import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bathing Water Quality Explorer", layout="wide")

st.title("🌊 Bathing Water Quality Explorer")
st.markdown("""
This tool enables the Environment Agency and partners to explore potential relationships between bacteria levels and environmental variables such as rainfall, tide height, and effluent discharges at designated bathing water sites.
""")

# File uploader
uploaded_file = st.file_uploader("Upload your data file (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            df = pd.read_csv(uploaded_file)

        st.success("File uploaded and read successfully!")

        # Basic preprocessing
        date_column = st.selectbox("Select the date/time column", df.columns)
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        df = df.dropna(subset=[date_column])

        site_column = st.selectbox("Select the site column (if available)", [col for col in df.columns if df[col].dtype == object])
        selected_site = st.selectbox("Choose a site to explore", df[site_column].unique())

        filtered_df = df[df[site_column] == selected_site]

        # Select variables to compare
        variable_1 = st.selectbox("Choose a variable to plot against time", df.select_dtypes(include='number').columns)
        variable_2 = st.selectbox("Choose a second variable to compare (e.g., E. coli, Rainfall)", df.select_dtypes(include='number').columns)

        st.subheader(f"Time Series of {variable_1} and {variable_2} at {selected_site}")
        fig, ax = plt.subplots()
        ax.plot(filtered_df[date_column], filtered_df[variable_1], label=variable_1)
        ax.set_ylabel(variable_1)
        ax.set_xlabel("Date")
        ax.legend(loc='upper left')

        ax2 = ax.twinx()
        ax2.plot(filtered_df[date_column], filtered_df[variable_2], color='orange', label=variable_2)
        ax2.set_ylabel(variable_2)
        ax2.legend(loc='upper right')

        st.pyplot(fig)

        st.subheader("Scatter Plot to Explore Relationships")
        st.write("This plot helps identify potential correlations between selected variables.")
        st.scatter_chart(filtered_df[[variable_1, variable_2]].dropna())

        st.subheader("Summary Statistics")
        st.write(filtered_df[[variable_1, variable_2]].describe())

        st.download_button("Download filtered data as CSV", filtered_df.to_csv(index=False), file_name=f"filtered_data_{selected_site}.csv")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")

else:
    st.info("Please upload a dataset to begin.")
