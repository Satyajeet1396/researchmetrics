import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import qrcode
import base64

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
st.write("Upload a CSV or Excel file containing a 'Cited by' column.")

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
            <p>Make sure your file contains a column named <strong>'Cited by'</strong>.</p>
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

    if "Cited by" in df.columns:
        citations = df["Cited by"].dropna().astype(int)
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
        st.error("The file does not contain a column named 'Cited by'. Please check your file.")
st.divider()
st.info("Created by Dr. Satyajeet Patil")
st.info("For more cool apps like this visit: https://patilsatyajeet.wixsite.com/home/python")

# Support section in expander
with st.expander("🤝 Support Our Research", expanded=False):
    st.markdown("""
        <div style='text-align: center; padding: 1rem; background-color: #f0f2f6; border-radius: 10px; margin: 1rem 0;'>
            <h3>🙏 Your Support Makes a Difference!</h3>
            <p>Your contribution helps us continue developing free tools for the research community.</p>
            <p>Every donation, no matter how small, fuels our research journey!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Two columns for QR code and Buy Me a Coffee button
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### UPI Payment")
        # Generate UPI QR code
        upi_url = "upi://pay?pa=satyajeet1396@oksbi&pn=Satyajeet Patil&cu=INR"
        qr = qrcode.make(upi_url)
        
        # Save QR code to BytesIO
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Display QR code with message
        st.markdown("Scan to pay: **satyajeet1396@oksbi**")
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center;">
                <img src="data:image/png;base64,{qr_base64}" width="200">
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown("#### Buy Me a Coffee")
        st.markdown("Support through Buy Me a Coffee platform:")
        # Buy Me a Coffee button
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <a href="https://www.buymeacoffee.com/researcher13" target="_blank">
                    <img src="https://img.buymeacoffee.com/button-api/?text=Support our Research&emoji=&slug=researcher13&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" alt="Support our Research"/>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

st.info("A small donation from you can fuel our research journey, turning ideas into breakthroughs that can change lives!")
