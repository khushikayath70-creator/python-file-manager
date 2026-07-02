"""
File Manager Studio
A clean Streamlit UI for local file operations.
"""

from datetime import datetime
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="File Manager Studio",
    page_icon="FM",
    layout="wide",
    initial_sidebar_state="expanded",
)

STORAGE_DIR = Path("user_files")
STORAGE_DIR.mkdir(exist_ok=True)


def list_files():
    return sorted([p for p in STORAGE_DIR.iterdir() if p.is_file()])


def human_size(num_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.0f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


def safe_file_path(name: str):
    clean_name = name.strip()

    if not clean_name:
        return None, "Please enter a file name."

    path = STORAGE_DIR / clean_name
    storage_root = STORAGE_DIR.resolve()

    try:
        resolved_path = path.resolve()
        resolved_path.relative_to(storage_root)
    except ValueError:
        return None, "Use a simple file name inside user_files only."

    if path.name in {"", ".", ".."}:
        return None, "Please enter a valid file name."

    return path, None


def apply_theme(theme_name: str):
    is_dark = theme_name == "Dark"

    if is_dark:
        colors = {
            "app_bg": "#101114",
            "app_bg_2": "#17191f",
            "surface": "#1d2027",
            "surface_2": "#242832",
            "sidebar": "#16181e",
            "border": "#343946",
            "text": "#f4f6fb",
            "muted": "#adb5c3",
            "soft": "#8892a3",
            "accent": "#7dd3fc",
            "primary": "#f4f6fb",
            "primary_text": "#101114",
            "input": "#12141a",
            "shadow": "rgba(0, 0, 0, 0.28)",
        }
    else:
        colors = {
            "app_bg": "#f7f8fb",
            "app_bg_2": "#eef1f5",
            "surface": "#ffffff",
            "surface_2": "#f4f6f8",
            "sidebar": "#ffffff",
            "border": "#e0e4ea",
            "text": "#1d2430",
            "muted": "#566173",
            "soft": "#7a8494",
            "accent": "#2563eb",
            "primary": "#1d2430",
            "primary_text": "#ffffff",
            "input": "#ffffff",
            "shadow": "rgba(20, 24, 33, 0.08)",
        }

    st.markdown(
        f"""
        <style>
        :root {{
            --app-bg: {colors["app_bg"]};
            --app-bg-2: {colors["app_bg_2"]};
            --surface: {colors["surface"]};
            --surface-2: {colors["surface_2"]};
            --sidebar: {colors["sidebar"]};
            --border: {colors["border"]};
            --text: {colors["text"]};
            --muted: {colors["muted"]};
            --soft: {colors["soft"]};
            --accent: {colors["accent"]};
            --primary: {colors["primary"]};
            --primary-text: {colors["primary_text"]};
            --input: {colors["input"]};
            --shadow: {colors["shadow"]};
        }}

        .stApp {{
            background: linear-gradient(180deg, var(--app-bg) 0%, var(--app-bg-2) 100%);
            color: var(--text);
        }}

        .block-container {{
            padding-top: 2rem;
            max-width: 1100px;
        }}

        .hero,
        .card,
        .stat-box {{
            background: var(--surface);
            border: 1px solid var(--border);
            box-shadow: 0 10px 30px var(--shadow);
        }}

        .hero {{
            padding: 28px 32px;
            border-radius: 8px;
            margin-bottom: 28px;
        }}

        .hero h1 {{
            color: var(--text);
            font-size: 1.9rem;
            font-weight: 700;
            letter-spacing: 0;
            margin: 0 0 6px 0;
        }}

        .hero p {{
            color: var(--muted);
            font-size: 0.98rem;
            margin: 0;
        }}

        .card {{
            border-radius: 8px;
            padding: 24px 26px;
            margin-bottom: 20px;
        }}

        .stat-box {{
            border-radius: 8px;
            padding: 16px 20px;
            text-align: center;
        }}

        .stat-num {{
            color: var(--text);
            font-size: 1.6rem;
            font-weight: 700;
            overflow-wrap: anywhere;
        }}

        .stat-label {{
            color: var(--soft);
            font-size: 0.8rem;
            letter-spacing: 0;
            text-transform: uppercase;
        }}

        .file-pill {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            background: var(--surface-2);
            color: var(--muted);
            border: 1px solid var(--border);
            font-size: 0.78rem;
            margin: 0 6px 6px 0;
        }}

        section[data-testid="stSidebar"] {{
            background: var(--sidebar);
            border-right: 1px solid var(--border);
        }}

        h1, h2, h3, h4, h5, h6,
        p, label, span,
        [data-testid="stMarkdownContainer"],
        [data-testid="stCaptionContainer"] {{
            color: var(--text);
        }}

        [data-testid="stCaptionContainer"],
        .st-emotion-cache-1v0mbdj,
        small {{
            color: var(--muted);
        }}

        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] textarea,
        div[data-baseweb="select"] > div {{
            background-color: var(--input);
            color: var(--text);
            border-color: var(--border);
        }}

        textarea,
        input {{
            color: var(--text) !important;
            caret-color: var(--accent);
        }}

        textarea:disabled {{
            -webkit-text-fill-color: var(--text);
            opacity: 1;
        }}

        div.stButton > button {{
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--surface-2);
            color: var(--text);
            font-weight: 600;
        }}

        div.stButton > button[kind="primary"] {{
            background: var(--primary);
            color: var(--primary-text);
            border: 1px solid var(--primary);
        }}

        hr {{
            border-color: var(--border);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


with st.sidebar:
    st.markdown("### Display")
    theme = st.radio(
        "Theme",
        ["Light", "Dark"],
        horizontal=True,
        label_visibility="collapsed",
    )

apply_theme(theme)

st.markdown(
    """
    <div class="hero">
        <h1>File Manager Studio</h1>
        <p>Create, read, update and delete files from a clean Python Streamlit interface.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

files = list_files()
total_size = sum(f.stat().st_size for f in files) if files else 0

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        f'<div class="stat-box"><div class="stat-num">{len(files)}</div>'
        f'<div class="stat-label">Total Files</div></div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f'<div class="stat-box"><div class="stat-num">{human_size(total_size)}</div>'
        f'<div class="stat-label">Storage Used</div></div>',
        unsafe_allow_html=True,
    )
with c3:
    latest = max(files, key=lambda f: f.stat().st_mtime).name if files else "-"
    st.markdown(
        f'<div class="stat-box"><div class="stat-num" style="font-size:1.1rem;">{latest}</div>'
        f'<div class="stat-label">Last Modified</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

st.sidebar.markdown("---")
st.sidebar.markdown("### Operations")
action = st.sidebar.radio(
    "Choose an action",
    ["Create File", "Read File", "Update File", "Delete File", "Browse All Files"],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.caption(f"Working directory: `{STORAGE_DIR.resolve().name}/`")

if action == "Create File":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Create a new file")

    name = st.text_input("File name", placeholder="e.g. notes.txt")
    content = st.text_area("File content", placeholder="Write something...", height=180)

    if st.button("Create File", type="primary"):
        path, error = safe_file_path(name)
        if error:
            st.warning(error)
        elif path.exists():
            st.error(f"'{path.name}' already exists. Choose a different name.")
        else:
            try:
                path.write_text(content, encoding="utf-8")
                st.success(f"File '{path.name}' created successfully.")
                st.rerun()
            except Exception as err:
                st.error(f"An error occurred: {err}")
    st.markdown("</div>", unsafe_allow_html=True)

elif action == "Read File":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Read a file")

    if not files:
        st.info("No files yet. Create one first.")
    else:
        chosen = st.selectbox("Select a file", [f.name for f in files])
        path = STORAGE_DIR / chosen
        try:
            content = path.read_text(encoding="utf-8")
            st.markdown(
                f'<span class="file-pill">{human_size(path.stat().st_size)}</span>'
                f'<span class="file-pill">Modified: '
                f'{datetime.fromtimestamp(path.stat().st_mtime).strftime("%d %b %Y, %H:%M")}</span>',
                unsafe_allow_html=True,
            )
            st.write("")
            st.text_area("Content", content, height=280, disabled=True)
        except Exception as err:
            st.error(f"An error occurred: {err}")
    st.markdown("</div>", unsafe_allow_html=True)

elif action == "Update File":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Update a file")

    if not files:
        st.info("No files yet. Create one first.")
    else:
        chosen = st.selectbox("Select a file", [f.name for f in files])
        path = STORAGE_DIR / chosen

        op = st.radio(
            "Choose operation",
            ["Rename", "Append content", "Overwrite content"],
            horizontal=True,
        )

        if op == "Rename":
            new_name = st.text_input("New file name")
            if st.button("Rename", type="primary"):
                new_path, error = safe_file_path(new_name)
                if error:
                    st.warning(error)
                elif new_path.exists():
                    st.error(f"'{new_path.name}' already exists.")
                else:
                    try:
                        path.rename(new_path)
                        st.success(f"Renamed to '{new_path.name}' successfully.")
                        st.rerun()
                    except Exception as err:
                        st.error(f"An error occurred: {err}")

        elif op == "Append content":
            add_text = st.text_area("Text to append", height=140)
            if st.button("Append", type="primary"):
                try:
                    with open(path, "a", encoding="utf-8") as fs:
                        fs.write("\n" + add_text)
                    st.success("Content appended successfully.")
                    st.rerun()
                except Exception as err:
                    st.error(f"An error occurred: {err}")

        elif op == "Overwrite content":
            new_text = st.text_area("New content (replaces everything)", height=180)
            if st.button("Overwrite", type="primary"):
                try:
                    path.write_text(new_text, encoding="utf-8")
                    st.success("File overwritten successfully.")
                    st.rerun()
                except Exception as err:
                    st.error(f"An error occurred: {err}")
    st.markdown("</div>", unsafe_allow_html=True)

elif action == "Delete File":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Delete a file")

    if not files:
        st.info("No files yet. Create one first.")
    else:
        chosen = st.selectbox("Select a file to delete", [f.name for f in files])
        st.warning("This action cannot be undone.")
        confirm = st.checkbox(f"I confirm I want to delete '{chosen}'")
        if st.button("Delete File", type="primary", disabled=not confirm):
            try:
                (STORAGE_DIR / chosen).unlink()
                st.success(f"'{chosen}' deleted successfully.")
                st.rerun()
            except Exception as err:
                st.error(f"An error occurred: {err}")
    st.markdown("</div>", unsafe_allow_html=True)

elif action == "Browse All Files":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("All files")

    if not files:
        st.info("No files yet. Create one to see it listed here.")
    else:
        for f in files:
            fc1, fc2, fc3 = st.columns([5, 2, 2])
            with fc1:
                st.markdown(f"**{f.name}**")
            with fc2:
                st.caption(human_size(f.stat().st_size))
            with fc3:
                st.caption(datetime.fromtimestamp(f.stat().st_mtime).strftime("%d %b %Y, %H:%M"))
            st.divider()
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Built with Python pathlib and Streamlit.")
