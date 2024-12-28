import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Function to calculate h-index
def calculate_h_index(citations):
    citations = sorted(citations, reverse=True)
    h_index = sum(1 for i, c in enumerate(citations) if i < c)
    return h_index

# Function to calculate i10-index
def calculate_i10_index(citations):
    return sum(1 for c in citations if c >= 10)

# Function to create a downloadable plot
def create_downloadable_plot(data, title, xlabel, ylabel):
    fig, ax = plt.subplots()
    ax.bar(range(len(data)), data)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer

# Streamlit UI
st.title("Research Metrics Calculator")
st.write("Upload a CSV or Excel file containing citations in index 12.")

uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx"])

if uploaded_file:
    # Load file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

    if 12 in df.columns or len(df.columns) > 12:
        citations = df.iloc[:, 12].dropna().astype(int)
        st.write("File loaded successfully!")
        st.write(df.head())

        # Calculate indices
        h_index = calculate_h_index(citations)
        i10_index = calculate_i10_index(citations)

        st.subheader("Results")
        st.write(f"h-index: {h_index}")
        st.write(f"i10-index: {i10_index}")

        # Generate and display plots
        st.subheader("Plots")
        buffer_h = create_downloadable_plot(citations, "Citations Distribution", "Papers", "Citations")
        st.pyplot(plt)

        # Download button for the plots
        st.download_button("Download Citations Plot", buffer_h, "citations_plot.png", "image/png")
    else:
        st.error("The file does not contain at least 13 columns (index 12). Please check your file.")
