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
        if page in lru_order:
            lru_order.move_to_end(page)
        else:
            page_faults += 1
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

# ---------- Background Motion + Pastel Color ----------
st.markdown("""
<style>

/* ---------- Smooth Animated Pastel Background ---------- */
@keyframes modernGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg,
        #ff9a9e 0%,
        #fad0c4 25%,
        #fbc2eb 50%,
        #a1c4fd 75%,
        #c2e9fb 100%
    );
    background-size: 400% 400%;
    animation: modernGradient 18s ease infinite;
}

/* ---------- Glassmorphism Card Style ---------- */
.block-container {
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(12px);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.50);
    backdrop-filter: blur(8px);
}

[data-testid="stSidebar"] .css-1d391kg {
    background: transparent !important;
}

/* Remove default white margins */
.main {
    background: transparent;
}

</style>
""", unsafe_allow_html=True)


# ---------- Title Section ----------
st.markdown(
    """
    <div style='text-align: center; padding: 20px;'>
        <h1 style='font-size: 55px; color: #6B5B95;'>⚙️ LRU Page Replacement Simulator</h1>
        <h3 style='color: #FF6F61;'>Visualize memory states with style!</h3>
    </div>
    """, unsafe_allow_html=True,
)

# ---------- Sidebar ----------
st.sidebar.title("📂 Upload Data & Settings")
csv_file = st.sidebar.file_uploader("Upload CSV file containing page sequence", type=["csv"])
frames = st.sidebar.slider("Number of Frames", min_value=1, max_value=10, value=3)

# ---------- Main App ----------
if csv_file:
    df = pd.read_csv(csv_file)
    st.subheader("📄 Original Data")
    st.dataframe(df, use_container_width=True)

    if "page" not in df.columns:
        st.error("CSV must contain a column named 'page'")
    else:
        pages = df["page"].tolist()
        history, faults = lru_page_replacement(pages, frames)
        st.subheader("📊 LRU Simulation Results")
        st.info(f"Simulation with **{frames} frames**")
        hist_df = pd.DataFrame(history)
        st.dataframe(hist_df, use_container_width=True)
        st.success(f"Total Page Faults: {faults}")
else:
    st.info("Upload a CSV file to begin simulation. Example with column 'page': [1,2,3,2,1,4,5]")
