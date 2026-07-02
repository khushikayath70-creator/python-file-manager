# 🗂️ File Manager Studio

A clean, premium-looking **Streamlit UI** built on top of a Python file-handling mini-project
(`pathlib` + `os`). Create, read, update, and delete files — all from a polished web interface
instead of a terminal menu.

## ✨ Features

- **Create** — make a new file with custom content
- **Read** — preview file content with size & last-modified info
- **Update** — rename, append content, or overwrite a file
- **Delete** — remove a file with a confirmation safeguard
- **Browse** — see all files at a glance with size & timestamp
- Live stats: total files, storage used, last modified file

## 🖥️ Tech Stack

- Python (`pathlib`, `os`)
- [Streamlit](https://streamlit.io/) for the UI

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd file_manager_app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`. All files are stored inside the local
`user_files/` folder.

## 📁 Project Structure

```
file_manager_app/
├── app.py              # Streamlit UI + file operations
├── requirements.txt    # Dependencies
├── README.md
└── user_files/         # Created files are stored here
```

## 📌 About

This project started as a simple CLI-based file handler (create/read/update/delete using
`pathlib` and `os`) and was upgraded into a fully interactive Streamlit web app with a
clean, light, card-based design.

---
Built with 🐍 Python + Streamlit.