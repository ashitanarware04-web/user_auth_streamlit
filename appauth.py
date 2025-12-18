import streamlit as st

# Page configuration
st.set_page_config(
    page_title="User Authentication System",
    page_icon="🔐",
    layout="centered"
)

# In-memory user database (dictionary)
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# App Title
st.markdown("<h1 style='text-align:center;'>🔐 User Authentication App</h1>", unsafe_allow_html=True)

# Sidebar menu
menu = ["Login", "Signup", "Dashboard", "About"]
choice = st.sidebar.radio("Navigation", menu)

# ---------------- SIGNUP ----------------
if choice == "Signup":
    st.subheader("📝 Create New Account")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if new_user == "" or new_pass == "":
            st.warning("⚠ Please fill all fields")
        elif new_user in st.session_state.users:
            st.error("❌ Username already exists")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("✅ Account created successfully")
            st.info("👉 Go to Login page")

# ---------------- LOGIN ----------------
elif choice == "Login":
    st.subheader("🔑 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user in st.session_state.users and st.session_state.users[user] == pwd:
            st.session_state.logged_in = True
            st.session_state.current_user = user
            st.success("✅ Login successful")
        else:
            st.error("❌ Invalid username or password")

# ---------------- DASHBOARD ----------------
elif choice == "Dashboard":
    if st.session_state.logged_in:
        st.subheader("🏠 Dashboard")
        st.success(f"Welcome, {st.session_state.current_user} 🎉")

        st.markdown("""
        ### What you can do:
        - View your profile
        - Access secure content
        - Logout safely
        """)

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.success("🚪 Logged out successfully")
    else:
        st.warning("⚠ Please login to access dashboard")

# ---------------- ABOUT ----------------
elif choice == "About":
    st.subheader("📘 About This Project")
    st.info("""
    *User Authentication Application*

    - Built using Python & Streamlit
    - Includes Signup, Login, Logout
    - Uses session-based authentication
    - Developed for internship assignment
    """)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>© Internship Project</p>", unsafe_allow_html=True)