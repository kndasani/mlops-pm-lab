import streamlit as st
from tutor import ask_tutor, get_knowledge_topics
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Strategy Mentor", page_icon="🔍", layout="centered")

# --- Performance: Cache the Knowledge Base Scan ---
@st.cache_data(ttl=3600)
def cached_topics():
    return get_knowledge_topics()

# --- CUSTOM CSS: Fixing the Topic Badges & Transitions ---
st.markdown("""
    <style>
    /* 1. Remove the 'Label' spacer that creates the misalignment */
    div[data-testid="stWidgetLabel"] {
        display: none !important;
    }

    /* 2. Force the row to align at the exact same bottom edge */
    [data-testid="column"] {
        display: flex !important;
        align-self: flex-end !important;
        padding-bottom: 0px !important;
    }

    /* 3. Sync the heights and remove any remaining internal margins */
    .stTextInput > div > div > input {
        height: 46px !important;
        margin-bottom: 0px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }

    .stButton > button {
        height: 46px !important;
        margin-top: 0px !important;
        margin-bottom: 0px !important;
        background-color: #1a73e8 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    .st-emotion-cache-zh2fnc{
        margin-top: auto;
        width: auto;
    }

    /* Explicit Chip Styling */
    .topic-chip {
        display: inline-block !important;
        background-color: #31333F !important; /* Professional dark grey for dark mode */
        border: 1px solid #4B4B4B !important;
        border-radius: 20px !important;
        padding: 6px 15px !important;
        margin: 6px !important; /* Creates the space between the words */
        font-size: 0.85rem !important;
        color: #E0E0E0 !important;
        white-space: nowrap !important; /* Prevents a single topic from breaking across lines */
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }

    /* 4. Results Card Contrast Fix */
    .result-container {
        padding: 24px;
        background-color: #ffffff !important;
        border-radius: 12px;
        border: 1px solid #dfe1e5;
        color: #202124 !important;
        margin-top: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .result-container * {
        color: #202124 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. State Management
if 'search_executed' not in st.session_state:
    st.session_state.search_executed = False

# 2. THE DYNAMIC VIEWPORT
if not st.session_state.search_executed:
    # --- DISCOVERY MODE (The "Home" Screen) ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>💡 Strategy Mentor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #70757a;'>Explain complex AI concept for your specific career path.</p>", unsafe_allow_html=True)
    
    # Inputs
    query = st.text_input("Search", placeholder="What is Model Drift?", label_visibility="collapsed")
    user_role = st.text_input("Role", placeholder="Your Role (e.g. Product Manager)", label_visibility="collapsed")
    
    # FIX: Clean Topic Cloud
    topics = cached_topics()
    if topics:
        st.write("")
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        # Display topics as a clean, wrapping list of chips
        topic_html = "".join([f'<span class="topic-chip">{t}</span>' for t in topics])
        st.markdown(topic_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if query and user_role:
        st.session_state.search_executed = True
        st.session_state.last_query = query
        st.session_state.last_role = user_role
        st.rerun()

else:
    # --- RESULTS MODE (The "SERP" Screen) ---
    st.markdown("<div class='compact-header'>💡 Strategy Mentor</div>", unsafe_allow_html=True)
    
    # Compact inputs at the top
    c1, c2, c3 = st.columns([3, 2, 1])
    with c1:
        new_query = st.text_input("", value=st.session_state.last_query, key="q_res")
    with c2:
        new_role = st.text_input("", value=st.session_state.last_role, key="r_res")
    with c3:
        if st.button("Search"):
            st.session_state.last_query = new_query
            st.session_state.last_role = new_role
            st.rerun()

    st.divider()

    # The Answer Section
    with st.spinner("Analyzing knowledge base..."):
        answer = ask_tutor(st.session_state.last_query, role=st.session_state.last_role)
    
    if answer:
        st.markdown(f"""
            <div class="result-container">
                <span style="color: #1a73e8; font-weight: bold;">Tailored Perspective: {st.session_state.last_role}</span>
                <p style="margin-top: 15px; color: #3c4043;">{answer}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("← New Search"):
        st.session_state.search_executed = False
        st.rerun()