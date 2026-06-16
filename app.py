import html
import re
import time

import streamlit as st
from agents import writer_chain, critic_chain
from pipeline import run_research_pipeline, run_url_pipeline


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchOS · Multi-Agent Research Intelligence",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root{
    --bg:#F7F9FC;
    --card:#FFFFFF;
    --soft:#F8FAFC;
    --text:#0F172A;
    --muted:#64748B;
    --muted2:#94A3B8;
    --border:#E2E8F0;
    --border2:#CBD5E1;
    --primary:#2563EB;
    --primary2:#0EA5E9;
    --success:#16A34A;
    --warning:#D97706;
    --danger:#DC2626;
    --shadow:0 18px 45px rgba(15,23,42,.08);
}

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
    color:var(--text);
}

.stApp{
    background:
        radial-gradient(circle at 8% 0%, rgba(37,99,235,.12), transparent 28%),
        radial-gradient(circle at 92% 8%, rgba(14,165,233,.10), transparent 30%),
        var(--bg);
}

#MainMenu, footer, header{visibility:hidden;}
.block-container{max-width:1180px;padding:1.35rem 1.8rem 3rem;}

/* Header */
.topbar{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:1rem;
    margin-bottom:1rem;
}
.brand{display:flex;align-items:center;gap:.72rem;}
.logo{
    width:42px;height:42px;border-radius:14px;
    display:grid;place-items:center;
    color:#fff;font-weight:900;letter-spacing:-.06em;
    background:linear-gradient(135deg,var(--primary),var(--primary2));
    box-shadow:0 12px 28px rgba(37,99,235,.24);
}
.brand-title{font-weight:900;font-size:1.08rem;letter-spacing:-.04em;}
.brand-sub{font-size:.79rem;color:var(--muted);margin-top:.06rem;}
.badge{
    border:1px solid var(--border);
    background:rgba(255,255,255,.75);
    padding:.48rem .75rem;border-radius:999px;
    font-size:.76rem;font-weight:700;color:#475569;
}

/* Compact hero */
.hero{
    background:linear-gradient(135deg,#FFFFFF 0%,#F8FBFF 100%);
    border:1px solid var(--border);
    border-radius:26px;
    box-shadow:var(--shadow);
    padding:2rem 2.15rem;
    position:relative;
    overflow:hidden;
    margin-bottom:1rem;
}
.hero:after{
    content:"";position:absolute;right:-120px;top:-120px;
    width:300px;height:300px;border-radius:999px;
    background:rgba(37,99,235,.08);
}
.kicker{
    display:inline-flex;align-items:center;gap:.42rem;
    padding:.42rem .72rem;border-radius:999px;
    color:var(--primary);font-size:.76rem;font-weight:800;
    background:#EFF6FF;border:1px solid #DBEAFE;
    margin-bottom:.95rem;
}
.hero h1{
    position:relative;z-index:1;
    font-size:clamp(2.15rem,4.6vw,4.1rem);
    line-height:1.02;margin:0;max-width:830px;
    letter-spacing:-.075em;font-weight:900;color:#0B1220;
}
.hero h1 span{color:var(--primary);}
.hero p{
    position:relative;z-index:1;
    max-width:740px;color:var(--muted);
    font-size:1rem;line-height:1.65;margin:.92rem 0 0;
}

/* Panels */
.grid{display:grid;grid-template-columns:1.12fr .88fr;gap:1rem;align-items:start;}
.panel{
    background:var(--card);
    border:1px solid var(--border);
    border-radius:24px;
    padding:1.35rem;
    box-shadow:0 14px 35px rgba(15,23,42,.065);
}
.panel-title{font-size:1.05rem;font-weight:900;letter-spacing:-.04em;margin-bottom:.25rem;}
.panel-copy{font-size:.88rem;color:var(--muted);line-height:1.55;margin-bottom:1rem;}

/* Mode selector */
div[role="radiogroup"]{gap:.5rem;}
.stRadio label{font-weight:700 !important;color:#334155 !important;}

/* Input */
.stTextInput label{display:none;}
.stTextInput > div[data-baseweb="input"]{
    background:#fff !important;
    border:1px solid #D1D5DB !important;
    border-radius:18px !important;
    height:66px !important;
    padding:0 22px !important;
    display:flex !important;
    align-items:center !important;
    box-shadow:0 1px 2px rgba(0,0,0,.04),0 8px 24px rgba(0,0,0,.05) !important;
}
.stTextInput > div[data-baseweb="input"]:focus-within{
    border:2px solid var(--primary) !important;
    box-shadow:0 0 0 4px rgba(37,99,235,.12),0 8px 24px rgba(0,0,0,.06) !important;
}
.stTextInput input{
    background:transparent !important;
    border:none !important;
    box-shadow:none !important;
    height:100% !important;
    color:var(--text) !important;
    font-size:17px !important;
    font-weight:500 !important;
    padding:0 !important;
}
.stTextInput input::placeholder{color:#94A3B8 !important;font-size:16px !important;font-weight:400 !important;opacity:1 !important;}

.stButton > button, .stDownloadButton > button{
    background:linear-gradient(135deg,var(--primary),var(--primary2)) !important;
    color:#fff !important;border:none !important;border-radius:16px !important;
    min-height:56px !important;font-weight:900 !important;font-size:.96rem !important;
    box-shadow:0 14px 28px rgba(37,99,235,.23) !important;
    transition:all .18s ease !important;
}
.stButton > button:hover, .stDownloadButton > button:hover{
    transform:translateY(-1px) !important;
    box-shadow:0 18px 34px rgba(37,99,235,.28) !important;
}

.small-note{font-size:.79rem;color:var(--muted);margin-top:.8rem;line-height:1.5;}
.chips{display:flex;gap:.45rem;flex-wrap:wrap;margin-top:.9rem;}
.chip{background:#F8FAFC;border:1px solid var(--border);border-radius:999px;padding:.34rem .65rem;font-size:.76rem;font-weight:700;color:#475569;}

/* Pipeline */
.step-card{display:flex;gap:.82rem;align-items:flex-start;border:1px solid var(--border);border-radius:16px;padding:.92rem;background:#F8FAFC;margin-bottom:.7rem;}
.step-card.running{background:#EFF6FF;border-color:#93C5FD;}
.step-card.done{background:#F0FDF4;border-color:#BBF7D0;}
.step-card.skip{opacity:.55;}
.step-num{width:2.08rem;height:2.08rem;border-radius:12px;display:grid;place-items:center;background:#E2E8F0;color:#334155;font-size:.78rem;font-weight:900;flex:0 0 auto;}
.step-card.running .step-num{background:#DBEAFE;color:var(--primary);}
.step-card.done .step-num{background:#DCFCE7;color:var(--success);}
.step-main{flex:1;}
.step-top{display:flex;align-items:center;justify-content:space-between;gap:.65rem;}
.step-title{font-size:.91rem;font-weight:900;color:var(--text);}
.step-desc{font-size:.8rem;color:var(--muted);line-height:1.42;margin-top:.16rem;}
.status{font-size:.67rem;font-weight:900;border-radius:999px;padding:.24rem .5rem;white-space:nowrap;background:#E2E8F0;color:#64748B;}
.status.running{background:#DBEAFE;color:#1D4ED8;}
.status.done{background:#DCFCE7;color:#15803D;}
.status.skip{background:#F1F5F9;color:#94A3B8;}

/* Output */
.output-title{font-size:1.45rem;font-weight:900;letter-spacing:-.045em;margin:1.55rem 0 .8rem;}
.report-card,.feedback-card,.raw-card{
    background:#fff;border:1px solid var(--border);border-radius:24px;
    padding:1.45rem;box-shadow:0 14px 35px rgba(15,23,42,.065);margin-bottom:1rem;
}
.report-card{border-top:5px solid var(--primary);}
.feedback-card{border-top:5px solid var(--success);}
.output-label{text-transform:uppercase;letter-spacing:.08em;font-size:.74rem;font-weight:900;color:var(--muted);margin-bottom:.75rem;}
.raw-text{white-space:pre-wrap;color:#334155;font-size:.9rem;line-height:1.65;}
.report-card p,.report-card li,.feedback-card p,.feedback-card li{color:#334155;line-height:1.7;}
.report-card h1,.report-card h2,.report-card h3{letter-spacing:-.035em;color:#0F172A;}
.stExpander{border:1px solid var(--border) !important;border-radius:16px !important;background:#fff !important;overflow:hidden !important;}
details summary{font-weight:900 !important;color:#334155 !important;}
.footer-note{text-align:center;color:var(--muted);font-size:.76rem;margin-top:2rem;}

@media(max-width:850px){
    .block-container{padding:1rem .9rem 2.5rem;}
    .topbar{flex-direction:column;align-items:flex-start;}
    .hero{padding:1.45rem;border-radius:22px;}
    .grid{grid-template-columns:1fr;}
}
</style>
""",
    unsafe_allow_html=True,
)


def safe_html(value):
    return html.escape(str(value))


def is_url(text: str) -> bool:
    return bool(re.match(r"^https?://", text.strip(), flags=re.IGNORECASE))


def step_card(num: str, title: str, state: str, desc: str):
    label = {"waiting": "Waiting", "running": "Running", "done": "Done", "skip": "Skipped"}.get(state, "Waiting")
    st.markdown(
        f"""
        <div class="step-card {state}">
            <div class="step-num">{num}</div>
            <div class="step-main">
                <div class="step-top">
                    <div class="step-title">{title}</div>
                    <div class="status {state}">{label}</div>
                </div>
                <div class="step-desc">{desc}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── State ───────────────────────────────────────────────────────────────────
for key in ("results", "running", "done", "mode"):
    if key not in st.session_state:
        if key == "results":
            st.session_state[key] = {}
        elif key == "mode":
            st.session_state[key] = "Research Topic"
        else:
            st.session_state[key] = False


# ── Header ──────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="topbar">
        <div class="brand">
            <div class="logo">RO</div>
            <div>
                <div class="brand-title">ResearchOS</div>
                <div class="brand-sub">Multi-Agent Research Intelligence Platform</div>
            </div>
        </div>
        <div class="badge">LangChain · Groq · Tavily · Streamlit</div>
    </div>

    <section class="hero">
        <div class="kicker">🔎 Autonomous Research Workspace</div>
        <h1>Research any topic or analyze any <span>URL with AI agents.</span></h1>
        <p>
            Search, read, write and critique using a clean multi-agent workflow designed
            for professional research reports.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)


# ── Main layout ─────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1.12, 0.88], gap="large")

with left_col:
    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">Start research</div>
            <div class="panel-copy">
                Choose whether you want autonomous topic research or direct URL analysis.
            </div>
        """,
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "Research mode",
        ["Research Topic", "Analyze URL"],
        horizontal=True,
        key="mode",
        label_visibility="collapsed",
    )

    placeholder = (
        "Ask a research question or explore a topic..."
        if mode == "Research Topic"
        else "Paste a URL to analyze, e.g. https://example.com/article"
    )

    user_input = st.text_input("", placeholder=placeholder, key="main_input")

    run_btn = st.button("Generate Research Report", use_container_width=True)

    if mode == "Research Topic":
        st.markdown(
            """
            <div class="chips">
                <span class="chip">AI agents in healthcare</span>
                <span class="chip">LangGraph use cases</span>
                <span class="chip">Fusion energy progress</span>
            </div>
            <div class="small-note">Topic mode uses Search Agent → Reader Agent → Writer → Critic.</div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="small-note">URL mode skips web search and directly analyzes the provided page using Reader → Writer → Critic.</div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">Pipeline status</div>
            <div class="panel-copy">Stages update based on the selected mode.</div>
        """,
        unsafe_allow_html=True,
    )

    r = st.session_state.results
    steps = ["search", "reader", "writer", "critic"]

    def state_for(step: str):
        if mode == "Analyze URL" and step == "search":
            return "skip"
        if step in r:
            return "done"
        if st.session_state.running:
            active_steps = ["reader", "writer", "critic"] if mode == "Analyze URL" else steps
            for k in active_steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent", state_for("search"), "Finds recent, reliable web information.")
    step_card("02", "Reader Agent", state_for("reader"), "Scrapes selected pages and extracts content.")
    step_card("03", "Writer Chain", state_for("writer"), "Creates a structured research report.")
    step_card("04", "Critic Chain", state_for("critic"), "Reviews the report and gives feedback.")

    st.markdown("</div>", unsafe_allow_html=True)


# ── Run pipeline ────────────────────────────────────────────────────────────
if run_btn:
    value = user_input.strip()
    if not value:
        st.warning("Please enter a topic or URL first.")
    elif mode == "Analyze URL" and not is_url(value):
        st.warning("Please enter a valid URL starting with http:// or https://")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.session_state.current_input = value
        st.session_state.current_mode = mode
        st.rerun()

if st.session_state.running and not st.session_state.done:
    value = st.session_state.current_input
    current_mode = st.session_state.current_mode

    with st.spinner("Running your research pipeline..."):
        if current_mode == "Analyze URL":
            results = run_url_pipeline(value)
            st.session_state.results = {
                "reader": results.get("scraped_content", ""),
                "writer": results.get("report", ""),
                "critic": results.get("feedback", ""),
            }
        else:
            results = run_research_pipeline(value)
            st.session_state.results = {
                "search": results.get("search_results", ""),
                "reader": results.get("scraped_content", ""),
                "writer": results.get("report", ""),
                "critic": results.get("feedback", ""),
            }

        if results.get("error"):
            st.session_state.results["error"] = results["error"]

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Output ──────────────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="output-title">Research Output</div>', unsafe_allow_html=True)

    if r.get("error"):
        st.error(r["error"])

    if r.get("writer"):
        st.markdown('<div class="report-card"><div class="output-label">Final Research Report</div>', unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            label="Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    if r.get("critic"):
        st.markdown('<div class="feedback-card"><div class="output-label">Critic Feedback</div>', unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown('</div>', unsafe_allow_html=True)

    if r.get("search"):
        with st.expander("View raw Search Agent output", expanded=False):
            st.markdown(f'<div class="raw-card"><div class="raw-text">{safe_html(r["search"])}</div></div>', unsafe_allow_html=True)

    if r.get("reader"):
        with st.expander("View raw Reader Agent output", expanded=False):
            st.markdown(f'<div class="raw-card"><div class="raw-text">{safe_html(r["reader"])}</div></div>', unsafe_allow_html=True)


st.markdown(
    """
    <div class="footer-note">
        ResearchOS · Powered by LangChain, Groq, Tavily and Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
