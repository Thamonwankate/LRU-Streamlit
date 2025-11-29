import streamlit as st
import pandas as pd
from collections import OrderedDict

# -----------------------------
# LRU PAGE REPLACEMENT FUNCTION
# -----------------------------
def lru_page_replacement(pages, frames):
    memory = []
    lru_order = OrderedDict()
    page_faults = 0
    history = []

    for page in pages:
        # If page already in memory → update LRU order
        if page in lru_order:
            lru_order.move_to_end(page)
        else:
            page_faults += 1
            # If memory is full → remove LRU page
            if len(lru_order) >= frames:
                old_page, _ = lru_order.popitem(last=False)
                memory.remove(old_page)
            memory.append(page)
            lru_order[page] = True

        history.append({
            "Page": page,
            "Memory State": memory.copy(),
            "Page Fault": page_faults
        })

    return history, page_faults

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="LRU Page Replacement", page_icon="📘", layout="wide")

# Modern UI Title Section
st.markdown(
    """
    <div style='text-align: center; padding: 20px;'>
        <h1 style='font-size: 55px; color: #3b82f6;'>⚙️ LRU Page Replacement Simulator</h1>
        <h3 style='color: #64748b;'>Simulate and visualize page replacement using LRU algorithm</h3>
    </div>
    """, unsafe_allow_html=True,
)

# -----------------------------
# Upload CSV File
# -----------------------------

st.sidebar.title("📂 Upload Data")
csv_file = st.sidebar.file_uploader("Upload CSV file containing page sequence", type=["csv"])
frames = st.sidebar.number_input("Number of Frames", 1, 10, 3)

if csv_file:
    df = pd.read_csv(csv_file)
    st.subheader("📄 Original Data")
    st.dataframe(df, use_container_width=True)

    # Expect column name "page"
    if "page" not in df.columns:
        st.error("CSV must contain a column named 'page'")
    else:
        pages = df["page"].tolist()

        # Run LRU
        history, faults = lru_page_replacement(pages, frames)
        st.subheader("📊 LRU Simulation Results")

        # Convert history to DataFrame
        hist_df = pd.DataFrame(history)
        st.dataframe(hist_df, use_container_width=True)

        st.success(f"Total Page Faults: {faults}")

else:
    st.info("Upload a CSV file to begin simulation. Example with column 'page': [1,2,3,2,1,4,5]")
