import streamlit as st
import sqlite3
import os
from datetime import date

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="NGO Media Page",
    layout="wide"
)

# --------------------------------------------------
# IMPORTANT NOTE (FOR INTERNSHIP REVIEW)
# --------------------------------------------------
# NOTE:
# Hardcoded admin credentials are used ONLY for demo/testing purposes.
# In real-world production systems, credentials should be stored securely
# in a database with password hashing and proper authentication mechanisms.

# Admin Credentials (Demo Only)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------
conn = sqlite3.connect("media.db", check_same_thread=False)
cur = conn.cursor()

# --------------------------------------------------
# DATABASE TABLES
# --------------------------------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS press_releases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    release_date DATE NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS media_coverage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS image_gallery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_url TEXT NOT NULL
)
""")

conn.commit()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

# --------------------------------------------------
# ADMIN LOGIN
# --------------------------------------------------
def admin_login():
    st.subheader("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.admin_logged = True
            st.success("Admin login successful")
        else:
            st.error("Invalid username or password")

# --------------------------------------------------
# FRONTEND: MEDIA PAGE
# --------------------------------------------------
def media_page():
    st.title("NGO Media Page")

    st.markdown("""
    **Welcome to our Media Page.**  
    This page highlights our NGO’s activities, achievements, and impact through
    press releases, media coverage, images, and videos.
    """)

    # ---------------- PRESS RELEASES ----------------
    st.header("📰 Press Releases")
    cur.execute("SELECT title, description, release_date FROM press_releases ORDER BY release_date DESC")
    releases = cur.fetchall()

    if releases:
        for pr in releases:
            st.subheader(pr[0])
            st.write(pr[1])
            st.caption(f"Date: {pr[2]}")
            st.divider()
    else:
        st.info("No press releases available.")

    # ---------------- MEDIA COVERAGE ----------------
    st.header("🌐 Media Coverage")
    cur.execute("SELECT title, url FROM media_coverage")
    coverage = cur.fetchall()

    if coverage:
        for mc in coverage:
            st.markdown(f"**{mc[0]}** — [View Article]({mc[1]})")
    else:
        st.info("No media coverage available.")

    # ---------------- IMAGE GALLERY ----------------
    st.header("🖼 Image Gallery")
    cur.execute("SELECT image_path FROM image_gallery")
    images = [img[0] for img in cur.fetchall()]

    if images:
        st.image(images, width=250)
    else:
        st.info("No images uploaded yet.")

    # ---------------- VIDEOS ----------------
    st.header("🎥 Videos")
    cur.execute("SELECT video_url FROM videos")
    videos = cur.fetchall()

    if videos:
        for v in videos:
            st.video(v[0])
    else:
        st.info("No videos available.")

    # ---------------- CONTACT ----------------
    st.markdown("---")
    st.markdown("📩 **Contact for Media:** media@ngo.org")

# --------------------------------------------------
# ADMIN DASHBOARD
# --------------------------------------------------
def admin_dashboard():
    st.title("Manage Media Page")

    tabs = st.tabs([
        "Press Releases",
        "Media Coverage",
        "Image Gallery",
        "Videos"
    ])

    # ---------------- PRESS RELEASE MANAGEMENT ----------------
    with tabs[0]:
        st.subheader("Add Press Release")

        title = st.text_input("Title")
        description = st.text_area("Description")
        release_date = st.date_input("Release Date", date.today())

        if st.button("Add Press Release"):
            cur.execute(
                "INSERT INTO press_releases VALUES (NULL, ?, ?, ?)",
                (title, description, release_date)
            )
            conn.commit()
            st.success("Press release added successfully")

        st.subheader("Existing Press Releases")
        cur.execute("SELECT id, title, release_date FROM press_releases")
        for pr in cur.fetchall():
            col1, col2 = st.columns([4, 1])
            col1.write(f"{pr[1]} ({pr[2]})")
            if col2.button("Delete", key=f"pr_{pr[0]}"):
                cur.execute("DELETE FROM press_releases WHERE id=?", (pr[0],))
                conn.commit()
                st.experimental_rerun()

    # ---------------- MEDIA COVERAGE MANAGEMENT ----------------
    with tabs[1]:
        st.subheader("Add Media Coverage")

        mc_title = st.text_input("Media Title")
        mc_url = st.text_input("Media URL")

        if st.button("Add Media Coverage"):
            cur.execute(
                "INSERT INTO media_coverage VALUES (NULL, ?, ?)",
                (mc_title, mc_url)
            )
            conn.commit()
            st.success("Media coverage added successfully")

        cur.execute("SELECT id, title FROM media_coverage")
        for mc in cur.fetchall():
            col1, col2 = st.columns([4, 1])
            col1.write(mc[1])
            if col2.button("Delete", key=f"mc_{mc[0]}"):
                cur.execute("DELETE FROM media_coverage WHERE id=?", (mc[0],))
                conn.commit()
                st.experimental_rerun()

    # ---------------- IMAGE GALLERY MANAGEMENT ----------------
    with tabs[2]:
        st.subheader("Upload Image")

        image = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

        if image:
            os.makedirs("uploads/gallery", exist_ok=True)
            path = f"uploads/gallery/{image.name}"

            with open(path, "wb") as f:
                f.write(image.getbuffer())

            cur.execute(
                "INSERT INTO image_gallery VALUES (NULL, ?)",
                (path,)
            )
            conn.commit()
            st.success("Image uploaded successfully")

        cur.execute("SELECT id, image_path FROM image_gallery")
        for img in cur.fetchall():
            col1, col2 = st.columns([4, 1])
            col1.image(img[1], width=150)
            if col2.button("Delete", key=f"img_{img[0]}"):
                cur.execute("DELETE FROM image_gallery WHERE id=?", (img[0],))
                conn.commit()
                st.experimental_rerun()

    # ---------------- VIDEO MANAGEMENT ----------------
    with tabs[3]:
        st.subheader("Add Video")

        video_url = st.text_input("Video URL (YouTube, etc.)")

        if st.button("Add Video"):
            cur.execute(
                "INSERT INTO videos VALUES (NULL, ?)",
                (video_url,)
            )
            conn.commit()
            st.success("Video added successfully")

        cur.execute("SELECT id, video_url FROM videos")
        for v in cur.fetchall():
            col1, col2 = st.columns([4, 1])
            col1.write(v[1])
            if col2.button("Delete", key=f"vid_{v[0]}"):
                cur.execute("DELETE FROM videos WHERE id=?", (v[0],))
                conn.commit()
                st.experimental_rerun()

# --------------------------------------------------
# MAIN NAVIGATION
# --------------------------------------------------
menu = st.sidebar.radio("Navigation", ["Media Page", "Admin"])

if menu == "Media Page":
    media_page()
else:
    if st.session_state.admin_logged:
        admin_dashboard()
    else:
        admin_login()
