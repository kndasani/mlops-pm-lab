import streamlit as st
from tutor import ask_tutor, get_knowledge_topics
from strategy_builder import build_strategy, analyze_context
from roadmap_renderer import generate_dashboard_html
from dotenv import load_dotenv
import os
import requests
import json
import streamlit.components.v1 as components

load_dotenv()

# Helper wrappers to hit the MCP server when the environment variable is set
MCP_URL = os.getenv("MCP_SERVER_URL")

def _remote_request(path: str, payload: dict):
    url = MCP_URL.rstrip("/") + path
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"MCP request failed: {e}")
        return None


def ask_tutor(question, role="Product Manager"):
    # if an MCP server is configured, delegate to it instead of running local code
    if MCP_URL:
        data = _remote_request("/mcp/v1/ask", {"question": question, "role": role})
        return data.get("answer") if data else None
    # fallback to original in-process implementation
    from tutor import generate_answer
    return generate_answer(question, role=role)


def get_knowledge_topics():
    if MCP_URL:
        data = _remote_request("/mcp/v1/topics", {})
        return data.get("topics") if data else []
    from tutor import get_knowledge_topics as _local_topics
    return _local_topics()


def build_user_strategy(context, resources, timeline, constraints, success_metrics):
    """Build strategy either via MCP or local."""
    if MCP_URL:
        data = _remote_request("/mcp/v1/strategy/build", {
            "context": context,
            "resources": resources,
            "timeline": timeline,
            "constraints": constraints,
            "success_metrics": success_metrics
        })
        return data.get("strategy") if data else None
    else:
        return build_strategy(context, resources, timeline, constraints, success_metrics)


def analyze_user_context(context):
    """Analyze context either via MCP or local."""
    if MCP_URL:
        data = _remote_request("/mcp/v1/strategy/analyze", {"context": context})
        return data.get("analysis") if data else None
    else:
        return analyze_context(context)

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
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = None  # None means showing home page with cards
if 'strategy_step' not in st.session_state:
    st.session_state.strategy_step = 1  # Multi-step form tracking


# 2. PAGE CONFIGURATION & HEADER
st.set_page_config(page_title="Strategy Mentor", page_icon="🔍", layout="wide")

# If app_mode is None, show the home page with cards
if st.session_state.app_mode is None:
    # ===== HOME PAGE WITH CARDS =====
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 42px;'>Strategy Mentor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #70757a; font-size: 18px; margin-bottom: 40px;'>Your AI learning and planning companion</p>", unsafe_allow_html=True)
    
    st.write("")
    
    # Two-column layout for cards
    col1, spacer, col2 = st.columns([1, 0.1, 1])
    
    with col1:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>❓ Ask a Question</h3>", unsafe_allow_html=True)
            st.markdown("""
            Ask specific questions about AI concepts, techniques, and applications based on your role and expertise level. 
            Get tailored explanations that match your career path and background.
            
            **Perfect for:**
            - Learning complex AI concepts
            - Understanding how AI applies to your role
            - Exploring new technologies relevant to your career
            """)
            if st.button("Start Asking Questions", key="ask_btn", use_container_width=True, type="primary"):
                st.session_state.app_mode = "ask"
                st.session_state.search_executed = False
                st.rerun()
    
    with col2:
        with st.container(border=True):
            st.markdown("<h3 style='margin-top: 0;'>🗺️ Build Your AI Strategy</h3>", unsafe_allow_html=True)
            st.markdown("""
            Create a personalized, actionable AI strategy tailored to your specific personal or professional goals. 
            Through a conversational interview, we'll build a phased roadmap just for you.
            
            **Perfect for:**
            - Defining your AI learning journey
            - Building an AI-powered business initiative
            - Creating a strategic implementation plan
            - Exploring how AI can help achieve your goals
            """)
            if st.button("Build Your Strategy", key="strategy_btn", use_container_width=True, type="primary"):
                st.session_state.app_mode = "strategy"
                st.session_state.strategy_step = 1
                st.rerun()

elif st.session_state.app_mode == "ask":
    # ===== ASK MODE (Original functionality) =====
    
    # Back button at the top
    if st.button("← Back to Home"):
        st.session_state.app_mode = None
        st.session_state.search_executed = False
        st.rerun()
    
    st.divider()
    
    if not st.session_state.search_executed:
        # --- DISCOVERY MODE (The "Home" Screen for Ask mode) ---
        st.markdown("<h1 style='text-align: center;'>💡 Ask a Question</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #70757a;'>Ask specific questions about AI concepts based on your career and expertise.</p>", unsafe_allow_html=True)
        
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
        st.markdown("<div class='compact-header'>💡 Ask a Question</div>", unsafe_allow_html=True)

        # Compact inputs at the top
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            new_query = st.text_input("", value=st.session_state.last_query, key="q_res")
        with c2:
            new_role = st.text_input("", value=st.session_state.last_role, key="r_res")
        with c3:
            search_button = st.button("Search", use_container_width=True)
            if search_button:
                st.session_state.last_query = new_query
                st.session_state.last_role = new_role
                st.rerun()

        st.divider()

        # The Answer Section with fixed layout
        st.markdown("<div style='min-height: 200px;'>", unsafe_allow_html=True)
        answer_placeholder = st.empty()
        with st.spinner("Analyzing knowledge base and generating answer..."):
            answer = ask_tutor(st.session_state.last_query, role=st.session_state.last_role)
        if answer:
            answer_placeholder.markdown(f"""
                <div class="result-container">
                    <span style="color: #1a73e8; font-weight: bold;">Tailored Perspective: {st.session_state.last_role}</span>
                    <p style="margin-top: 15px; color: #3c4043;">{answer}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            answer_placeholder.markdown("<div class='result-container'><em>No answer found.</em></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        if st.button("← New Search"):
            st.session_state.search_executed = False
            st.rerun()

else:
    # ===== STRATEGY MODE (New functionality) =====
    
    # Back button at the top
    if st.button("← Back to Home"):
        st.session_state.app_mode = None
        st.session_state.strategy_step = 1
        st.rerun()
    
    st.divider()
    
    st.markdown("# 🗺️ Build Your AI Strategy")
    st.markdown("*Let's have a conversation about your goals and create a personalized roadmap.*")
    st.write("")
    
    # Conversational flow
    if st.session_state.strategy_step == 1:
        # STEP 1: Get initial context
        st.subheader("Tell me about your situation")
        st.write("Be as specific as you can - what are you trying to achieve and in what context?")
        st.write("")
        
        context = st.text_area(
            "Your situation:",
            placeholder="E.g., I'm a bookstore owner looking to increase sales using AI-powered recommendations. I have very limited tech knowledge.",
            height=100,
            label_visibility="collapsed"
        )
        
        if st.button("Let's explore this →", type="primary", use_container_width=True):
            if context.strip():
                st.session_state.strategy_context = context
                
                # Analyze context to get follow-up questions
                with st.spinner("Analyzing your situation..."):
                    analysis = analyze_user_context(context)
                
                if analysis:
                    st.session_state.strategy_analysis = analysis
                    st.session_state.strategy_step = 2
                    st.rerun()
            else:
                st.error("Please describe your situation to continue.")
    
    elif st.session_state.strategy_step == 2:
        # STEP 2: Follow-up questions based on their context
        analysis = st.session_state.get("strategy_analysis", {})
        followup_questions = analysis.get("follow_up_questions", [
            "What are your expectations for AI?",
            "How much do you know about AI?",
            "What concerns do you have?"
        ])
        
        st.subheader("Great! I have a few questions to better understand your needs")
        st.write(f"**Your role:** {analysis.get('inferred_role', 'Professional')}")
        st.write(f"**Your goal:** {analysis.get('primary_goal', 'AI integration')}")
        st.write("")
        
        # Show first 2-3 follow-up questions
        answers = {}
        for i, question in enumerate(followup_questions[:3]):
            st.write(f"**{question}**")
            answers[f"answer_{i}"] = st.text_area(
                f"Your response:",
                placeholder="Type your answer here...",
                height=70,
                label_visibility="collapsed",
                key=f"followup_{i}"
            )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.strategy_step = 1
                st.rerun()
        with col2:
            if st.button("Generate My Strategy →", type="primary", use_container_width=True):
                # Combine all answers into context
                followup_context = "\n".join([
                    f"Q: {question}\nA: {answers.get(f'answer_{i}', 'Not answered')}"
                    for i, question in enumerate(followup_questions[:3])
                ])
                st.session_state.followup_answers = followup_context
                st.session_state.strategy_step = 3
                st.rerun()
    
    elif st.session_state.strategy_step == 3:
        # STEP 3: Generate strategy
        st.subheader("Creating your personalized AI strategy...")
        
        with st.spinner("Analyzing your situation and generating roadmap..."):
            analysis = st.session_state.get("strategy_analysis", {})
            followup = st.session_state.get("followup_answers", "")
            
            strategy = build_strategy(
                user_context=st.session_state.strategy_context + "\n\n--- Follow-up Details ---\n" + followup,
                resources=analysis.get('inferred_role', 'Not specified'),
                timeline=analysis.get('context_type', 'Not specified'),
                constraints=analysis.get('maturity_estimate', 'Not specified'),
                success_metrics=followup
            )
        
        if strategy:
            st.session_state.last_strategy = strategy
            st.session_state.strategy_step = 4
            st.rerun()
        else:
            st.error("❌ Could not generate strategy. Please try again.")
            if st.button("← Start Over"):
                st.session_state.strategy_step = 1
                st.rerun()
    
    elif st.session_state.strategy_step == 4:
        # STEP 4: Display strategy dashboard
        st.write("")  # Spacing
        
        # Render dashboard using Streamlit's HTML component
        dashboard_html = generate_dashboard_html(st.session_state.last_strategy)
        components.html(dashboard_html, height=4000, scrolling=True)
        
        # Export options
        st.write("")
        st.divider()
        st.subheader("📥 Export Your Strategy")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download as markdown
            from strategy_builder import strategy_to_markdown
            markdown_content = strategy_to_markdown(st.session_state.last_strategy)
            st.download_button(
                label="📄 Download as Markdown",
                data=markdown_content,
                file_name=f"AI_Strategy_{st.session_state.last_strategy['context_analysis'].get('inferred_role', 'Strategy').replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col2:
            # Download as JSON
            json_content = json.dumps(st.session_state.last_strategy, indent=2)
            st.download_button(
                label="⚙️ Download as JSON",
                data=json_content,
                file_name=f"AI_Strategy_{st.session_state.last_strategy['context_analysis'].get('inferred_role', 'Strategy').replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            if st.button("← Start New Strategy", use_container_width=True):
                st.session_state.strategy_step = 1
                st.rerun()
