import streamlit as st
import sqlite3

# ---------------- DATABASE ----------------
def get_connection():
    return sqlite3.connect("ngo_about_v2.db", check_same_thread=False)

conn = get_connection()
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS story (text TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS core_values (value TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS programs (program TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS team (name TEXT, role TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS impact (detail TEXT)")
conn.commit()

# ---------------- SEED DATA ----------------
def insert_default_data():
    if cur.execute("SELECT COUNT(*) FROM story").fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO story VALUES ('We are a non-profit organization working for social development.')"
        )

    if cur.execute("SELECT COUNT(*) FROM core_values").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO core_values VALUES (?)",
            [("Transparency",), ("Empathy",), ("Community Service",)]
        )

    if cur.execute("SELECT COUNT(*) FROM programs").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO programs VALUES (?)",
            [("Child Education",), ("Free Medical Checkups",), ("Skill Development",)]
        )

    if cur.execute("SELECT COUNT(*) FROM team").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO team VALUES (?,?)",
            [("Amit Kulkarni", "Director"), ("Pooja Deshmukh", "Manager")]
        )

    if cur.execute("SELECT COUNT(*) FROM impact").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO impact VALUES (?)",
            [("5,000+ lives impacted",), ("50+ active volunteers",)]
        )

    conn.commit()

insert_default_data()

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- SIDEBAR ----------------
st.sidebar.title("NGO Management")
menu = st.sidebar.radio("Navigate", ["About Us", "Admin Login"])

# ---------------- ABOUT US ----------------
def about_us_page():
    st.title("🌍 About Our NGO")
    st.write("Building a better future together")

    st.subheader("📘 Our Story")
    st.info(cur.execute("SELECT text FROM story").fetchone()[0])

    st.subheader("⭐ Core Values")
    for val in cur.execute("SELECT value FROM core_values"):
        st.write("•", val[0])

    st.subheader("🛠 Our Programs")
    for p in cur.execute("SELECT program FROM programs"):
        st.write("•", p[0])

    st.subheader("👥 Our Team")
    for t in cur.execute("SELECT name, role FROM team"):
        st.write(f"{t[0]}** – {t[1]}")

    st.subheader("📊 Impact")
    for i in cur.execute("SELECT detail FROM impact"):
        st.write("•", i[0])

    col1, col2 = st.columns(2)
    col1.button("Donate Now")
    col2.button("Become a Volunteer")

# ---------------- ADMIN PANEL ----------------
def admin_panel():
    st.title("🔐 Admin Dashboard")

    st.markdown("### Update Story")
    story_text = st.text_area(
        "Story",
        cur.execute("SELECT text FROM story").fetchone()[0]
    )

    if st.button("Update Story"):
        cur.execute("DELETE FROM story")
        cur.execute("INSERT INTO story VALUES (?)", (story_text,))
        conn.commit()
        st.success("Story updated successfully")

    st.markdown("### Add Core Value")
    value = st.text_input("Core Value")
    if st.button("Save Value"):
        cur.execute("INSERT INTO core_values VALUES (?)", (value,))
        conn.commit()
        st.success("Value added")

    st.markdown("### Add Program")
    program = st.text_input("Program")
    if st.button("Save Program"):
        cur.execute("INSERT INTO programs VALUES (?)", (program,))
        conn.commit()
        st.success("Program added")

    st.markdown("### Add Team Member")
    name = st.text_input("Name")
    role = st.text_input("Role")
    if st.button("Save Team Member"):
        cur.execute("INSERT INTO team VALUES (?,?)", (name, role))
        conn.commit()
        st.success("Team member added")

# ---------------- PAGE LOGIC ----------------
if menu == "About Us":
    about_us_page()

elif menu == "Admin Login":
    if not st.session_state.logged_in:
        st.subheader("Admin Login")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if u == "admin" and p == "admin123":
                st.session_state.logged_in = True
                st.success("Login successful")
            else:
                st.error("Wrong credentials")

    if st.session_state.logged_in:
        admin_panel()