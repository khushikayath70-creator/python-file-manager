"""
File Manager Studio
A clean, premium Streamlit UI for local file operations
(Create / Read / Update / Delete) built on top of pathlib + os.
"""

from pathlib import Path
from datetime import datetime
import streamlit as st

# ------------------------------------------------------------------
# App config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="File Manager Studio",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

STORAGE_DIR = Path("user_files")
STORAGE_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------------
# Styling — light, premium, well structured
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #fafafa 0%, #f4f5f7 100%);
    }
    .block-container {
        padding-top: 2rem;
        max-width: 1100px;
    }
    .hero {
        padding: 28px 32px;
        border-radius: 18px;
        background: linear-gradient(135deg, #ffffff 0%, #f7f8fa 100%);
        border: 1px solid #eaeaec;
        box-shadow: 0 4px 24px rgba(20, 20, 30, 0.04);
        margin-bottom: 28px;
    }
    .hero h1 {
        font-size: 1.9rem;
        font-weight: 700;
        margin-bottom: 4px;
        color: #1a1a1f;
    }
    .hero p {
        color: #6b6b76;
        font-size: 0.98rem;
        margin: 0;
    }
    .card {
        background: #ffffff;
        border: 1px solid #eceef1;
        border-radius: 16px;
        padding: 24px 26px;
        box-shadow: 0 2px 12px rgba(20, 20, 30, 0.03);
        margin-bottom: 20px;
    }
    .stat-box {
        background: #ffffff;
        border: 1px solid #eceef1;
        border-radius: 14px;
        padding: 16px 20px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(20, 20, 30, 0.03);
    }
    .stat-num {
        font-size: 1.6rem;
        font-weight: 700;
        color: #2b2b33;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #8a8a94;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #ececee;
    }
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        border: 1px solid #e2e2e6;
    }
    div.stButton > button[kind="primary"] {
        background: #1f1f27;
        color: white;
        border: none;
    }
    .file-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        background: #f1f1f4;
        color: #4a4a52;
        font-size: 0.78rem;
        margin-right: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def list_files():
    return sorted([p for p in STORAGE_DIR.iterdir() if p.is_file()])


def human_size(num_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.0f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


def refresh():
    st.rerun()


# ------------------------------------------------------------------
# Hero header
# ------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🗂️ File Manager Studio</h1>
        <p>Create, read, update and delete files — a clean interface over Python's
        <code>pathlib</code> &amp; <code>os</code> file handling basics.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Stats row
# ------------------------------------------------------------------
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
    latest = max(files, key=lambda f: f.stat().st_mtime).name if files else "—"
    st.markdown(
        f'<div class="stat-box"><div class="stat-num" style="font-size:1.1rem;">{latest}</div>'
        f'<div class="stat-label">Last Modified</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

# ------------------------------------------------------------------
# Sidebar navigation
# ------------------------------------------------------------------
st.sidebar.markdown("### Operations")
action = st.sidebar.radio(
    "Choose an action",
    ["📄 Create File", "📖 Read File", "✏️ Update File", "🗑️ Delete File", "📁 Browse All Files"],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.caption(f"Working directory: `{STORAGE_DIR.resolve().name}/`")

# ------------------------------------------------------------------
# CREATE
# ------------------------------------------------------------------
if action == "📄 Create File":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Create a new file")

    name = st.text_input("File name", placeholder="e.g. notes.txt")
    content = st.text_area("File content", placeholder="Write something...", height=180)

    if st.button("Create File", type="primary"):
        if not name.strip():
            st.warning("Please enter a file name.")
        else:
            path = STORAGE_DIR / name
            if path.exists():
                st.error(f"'{name}' already exists. Choose a different name.")
            else:
                try:
                    path.write_text(content)
                    st.success(f"File '{name}' created successfully ✅")
                except Exception as err:
                    st.error(f"An error occurred: {err}")
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# READ
# ------------------------------------------------------------------
elif action == "📖 Read File":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Read a file")

    if not files:
        st.info("No files yet. Create one first.")
    else:
        chosen = st.selectbox("Select a file", [f.name for f in files])
        path = STORAGE_DIR / chosen
        try:
            content = path.read_text()
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

# ------------------------------------------------------------------
# UPDATE
# ------------------------------------------------------------------
elif action == "✏️ Update File":
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
                new_path = STORAGE_DIR / new_name
                if not new_name.strip():
                    st.warning("Enter a new name.")
                elif new_path.exists():
                    st.error(f"'{new_name}' already exists.")
                else:
                    try:
                        path.rename(new_path)
                        st.success(f"Renamed to '{new_name}' successfully ✅")
                    except Exception as err:
                        st.error(f"An error occurred: {err}")

        elif op == "Append content":
            add_text = st.text_area("Text to append", height=140)
            if st.button("Append", type="primary"):
                try:
                    with open(path, "a") as fs:
                        fs.write("\n" + add_text)
                    st.success("Content appended successfully ✅")
                except Exception as err:
                    st.error(f"An error occurred: {err}")

        elif op == "Overwrite content":
            new_text = st.text_area("New content (replaces everything)", height=180)
            if st.button("Overwrite", type="primary"):
                try:
                    path.write_text(new_text)
                    st.success("File overwritten successfully ✅")
                except Exception as err:
                    st.error(f"An error occurred: {err}")
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# DELETE
# ------------------------------------------------------------------
elif action == "🗑️ Delete File":
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
                st.success(f"'{chosen}' deleted successfully ✅")
                st.rerun()
            except Exception as err:
                st.error(f"An error occurred: {err}")
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# BROWSE ALL
# ------------------------------------------------------------------
elif action == "📁 Browse All Files":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("All files")

    if not files:
        st.info("No files yet. Create one to see it listed here.")
    else:
        for f in files:
            fc1, fc2, fc3 = st.columns([5, 2, 2])
            with fc1:
                st.markdown(f"**📄 {f.name}**")
            with fc2:
                st.caption(human_size(f.stat().st_size))
            with fc3:
                st.caption(datetime.fromtimestamp(f.stat().st_mtime).strftime("%d %b %Y, %H:%M"))
            st.divider()
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Built with Python (pathlib, os) + Streamlit — a simple file handling mini-project.")