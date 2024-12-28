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

# Expandable container with custom styling
with st.expander("ℹ️ Click here to learn about this app", expanded=False):
    st.markdown("""
        <style>
        .app-info {
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f2f6;
            margin: 10px 0;
        }
        .app-info h3 {
            color: #0066cc;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .app-info ul, .app-info ol {
            margin-bottom: 20px;
        }
        </style>
        <div class="app-info">
            <h3>About This App</h3>
            <p>This app calculates <strong>h-index</strong> and <strong>i10-index</strong> from a list of citations provided in a CSV or Excel file.</p>
            <ul>
                <li><strong>h-index</strong>: The largest number <em>h</em> such that at least <em>h</em> papers have <em>h</em> or more citations.</li>
                <li><strong>i10-index</strong>: The number of papers with at least 10 citations.</li>
            </ul>
            <p><strong>Features:</strong></p>
            <ol>
                <li>Upload your citation data.</li>
                <li>Visualize the citation distribution using a bar chart.</li>
                <li>Download the generated plots for your records.</li>
            </ol>
            <p>Make sure your file contains at least 13 columns, with citations located in column index 12.</p>
        </div>
        """, unsafe_allow_html=True)

# File uploader
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
