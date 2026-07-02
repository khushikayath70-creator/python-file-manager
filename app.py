"""
File Manager Studio
A clean Streamlit UI for local file operations.
"""

from datetime import datetime
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="File Manager Studio",
    page_icon=":material/folder:",
    layout="wide",
    initial_sidebar_state="expanded",
)

STORAGE_DIR = Path("user_files")
STORAGE_DIR.mkdir(exist_ok=True)


def list_files():
    return sorted([p for p in STORAGE_DIR.iterdir() if p.is_file() and p.name != ".gitkeep"])


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
            "accent_text": "#0f172a",
            "primary": "#f4f6fb",
            "primary_text": "#101114",
            "input": "#12141a",
            "input_focus": "#263244",
            "shadow": "rgba(0, 0, 0, 0.28)",
            "success_bg": "#123524",
            "warning_bg": "#3a2b10",
            "error_bg": "#3b1518",
            "info_bg": "#102b3a",
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
            "accent_text": "#ffffff",
            "primary": "#1d2430",
            "primary_text": "#ffffff",
            "input": "#ffffff",
            "input_focus": "#edf4ff",
            "shadow": "rgba(20, 24, 33, 0.08)",
            "success_bg": "#eaf7ef",
            "warning_bg": "#fff7e6",
            "error_bg": "#fdecec",
            "info_bg": "#eaf4ff",
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
            --accent-text: {colors["accent_text"]};
            --primary: {colors["primary"]};
            --primary-text: {colors["primary_text"]};
            --input: {colors["input"]};
            --input-focus: {colors["input_focus"]};
            --shadow: {colors["shadow"]};
            --success-bg: {colors["success_bg"]};
            --warning-bg: {colors["warning_bg"]};
            --error-bg: {colors["error_bg"]};
            --info-bg: {colors["info_bg"]};
        }}

        html,
        body,
        .stApp {{
            background: linear-gradient(180deg, var(--app-bg) 0%, var(--app-bg-2) 100%);
            color: var(--text);
        }}

        header[data-testid="stHeader"] {{
            background: transparent;
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

        section[data-testid="stSidebar"] * {{
            color: var(--text);
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

        code {{
            color: var(--accent);
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 2px 5px;
        }}

        section[data-testid="stSidebar"] code {{
            color: var(--text);
            background: var(--surface-2);
            border-color: var(--border);
        }}

        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div,
        div[data-baseweb="select"] > div {{
            background-color: var(--input);
            border-color: var(--border);
        }}

        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea,
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] input,
        div[data-baseweb="select"] div {{
            color: var(--text) !important;
            -webkit-text-fill-color: var(--text) !important;
        }}

        div[data-baseweb="input"] > div:focus-within,
        div[data-baseweb="textarea"] > div:focus-within,
        div[data-baseweb="select"] > div:focus-within {{
            background-color: var(--input-focus);
            border-color: var(--border);
            box-shadow: 0 0 0 1px var(--accent);
        }}

        textarea,
        input,
        [data-baseweb="select"] input {{
            color: var(--text) !important;
            -webkit-text-fill-color: var(--text) !important;
            caret-color: var(--accent);
        }}

        textarea:disabled {{
            -webkit-text-fill-color: var(--text);
            opacity: 1;
        }}

        input::placeholder,
        textarea::placeholder {{
            color: var(--soft) !important;
            opacity: 1;
        }}

        [data-baseweb="radio"] div {{
            color: var(--text);
        }}

        [data-baseweb="radio"] [aria-checked="true"] div:first-child {{
            border-color: var(--accent);
            background-color: var(--accent);
        }}

        div[data-baseweb="popover"],
        div[data-baseweb="popover"] > div,
        div[data-baseweb="menu"],
        ul[role="listbox"],
        div[role="listbox"] {{
            background: var(--surface) !important;
            border-color: var(--border) !important;
            color: var(--text) !important;
        }}

        div[role="option"],
        li[role="option"],
        ul[role="listbox"] li,
        div[data-baseweb="menu"] li {{
            background: var(--surface) !important;
            color: var(--text) !important;
        }}

        div[role="option"] *,
        li[role="option"] *,
        ul[role="listbox"] li *,
        div[data-baseweb="menu"] li * {{
            color: var(--text) !important;
        }}

        div[role="option"]:hover,
        li[role="option"]:hover,
        div[role="option"][aria-selected="true"],
        li[role="option"][aria-selected="true"] {{
            background: var(--surface-2) !important;
        }}

        div.stButton > button {{
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--surface-2);
            color: var(--text);
            font-weight: 600;
        }}

        div.stButton > button *,
        div.stButton > button p,
        div.stButton > button span {{
            color: var(--text) !important;
        }}

        div.stButton > button[kind="primary"] {{
            background: var(--primary);
            color: var(--primary-text) !important;
            border: 1px solid var(--primary);
        }}

        div.stButton > button[kind="primary"] *,
        div.stButton > button[kind="primary"] p,
        div.stButton > button[kind="primary"] span {{
            color: var(--primary-text) !important;
        }}

        div.stButton > button:hover {{
            border-color: var(--accent);
            color: var(--accent) !important;
        }}

        div.stButton > button:hover *,
        div.stButton > button:hover p,
        div.stButton > button:hover span {{
            color: var(--accent) !important;
        }}

        div.stButton > button[kind="primary"]:hover {{
            background: var(--accent);
            border-color: var(--accent);
            color: var(--accent-text) !important;
        }}

        div.stButton > button[kind="primary"]:hover *,
        div.stButton > button[kind="primary"]:hover p,
        div.stButton > button[kind="primary"]:hover span {{
            color: var(--accent-text) !important;
        }}

        [data-testid="stAlert"] {{
            border: 1px solid var(--border);
            color: var(--text);
        }}

        [data-testid="stAlert"] * {{
            color: var(--text);
        }}

        [data-testid="stExpander"] {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
        }}

        [data-testid="stExpander"] summary {{
            color: var(--text);
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

    if "expanded_files" not in st.session_state:
        st.session_state.expanded_files = set()

    if not files:
        st.info("No files yet. Create one to see it listed here.")
    else:
        for f in files:
            size_txt = human_size(f.stat().st_size)
            time_txt = datetime.fromtimestamp(f.stat().st_mtime).strftime("%d %b %Y, %H:%M")
            is_open = f.name in st.session_state.expanded_files

            fc0, fc1, fc2, fc3 = st.columns([0.4, 4.6, 2, 2])
            with fc0:
                arrow = "▾" if is_open else "▸"
                if st.button(arrow, key=f"toggle_{f.name}"):
                    if is_open:
                        st.session_state.expanded_files.discard(f.name)
                    else:
                        st.session_state.expanded_files.add(f.name)
                    st.rerun()
            with fc1:
                if st.button(f.name, key=f"toggle_name_{f.name}"):
                    if is_open:
                        st.session_state.expanded_files.discard(f.name)
                    else:
                        st.session_state.expanded_files.add(f.name)
                    st.rerun()
            with fc2:
                st.caption(size_txt)
            with fc3:
                st.caption(time_txt)

            if is_open:
                try:
                    file_content = f.read_text(encoding="utf-8")
                    st.text_area(
                        "Content",
                        file_content,
                        height=200,
                        disabled=True,
                        key=f"preview_{f.name}",
                        label_visibility="collapsed",
                    )
                except Exception as err:
                    st.error(f"Could not open file: {err}")

            st.divider()
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Built with Python pathlib and Streamlit.")
