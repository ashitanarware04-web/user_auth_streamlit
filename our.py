import streamlit as st
import sqlite3
import os
from datetime import date

# ---------- DATABASE ----------
conn = sqlite3.connect("ngo.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    status TEXT,
    start_date TEXT,
    end_date TEXT,
    location TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS project_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    image_path TEXT
)
""")

conn.commit()

# ---------- UPLOAD FOLDER ----------
if not os.path.exists("uploads"):
    os.mkdir("uploads")

# ---------- SIDEBAR ----------
st.sidebar.title("NGO Dashboard")
page = st.sidebar.radio("Go to", ["Our Projects", "Admin Panel"])

# ================= OUR PROJECTS =================
if page == "Our Projects":
    st.title("Our Projects")
    st.write("Making a difference through our initiatives")

    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Ongoing", "Completed", "Upcoming"]
    )

    if status_filter == "All":
        cur.execute("SELECT * FROM projects")
    else:
        cur.execute("SELECT * FROM projects WHERE status=?", (status_filter,))

    projects = cur.fetchall()

    for p in projects:
        st.subheader(p[1])
        st.write(p[2])
        st.write("📍 Location:", p[6])
        st.write("📅 Status:", p[3])

        cur.execute("SELECT image_path FROM project_images WHERE project_id=?", (p[0],))
        images = cur.fetchall()

        for img in images:
            st.image(img[0], width=300)

        st.markdown("---")

# ================= ADMIN PANEL =================
if page == "Admin Panel":
    st.title("Admin – Manage Projects")

    with st.form("add_project"):
        title = st.text_input("Project Title")
        desc = st.text_area("Description")
        status = st.selectbox("Status", ["Ongoing", "Completed", "Upcoming"])
        start = st.date_input("Start Date", date.today())
        end = st.date_input("End Date", date.today())
        location = st.text_input("Location")

        submit = st.form_submit_button("Add Project")

        if submit:
            cur.execute(
                "INSERT INTO projects VALUES (NULL,?,?,?,?,?,?)",
                (title, desc, status, str(start), str(end), location)
            )
            conn.commit()
            st.success("Project Added Successfully")

    st.subheader("Upload Project Images")

    cur.execute("SELECT id, title FROM projects")
    project_list = cur.fetchall()

    project_dict = {}
    for p in project_list:
        project_dict[p[1]] = p[0]

    project_name = st.selectbox("Select Project", project_dict.keys())
    image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if st.button("Upload Image"):
        if image:
            path = f"uploads/{image.name}"
            with open(path, "wb") as f:
                f.write(image.read())

            cur.execute(
                "INSERT INTO project_images VALUES (NULL,?,?)",
                (project_dict[project_name], path)
            )
            conn.commit()
            st.success("Image Uploaded")

# ---------- FOOTER ----------
st.sidebar.info("NGO Project Management System")