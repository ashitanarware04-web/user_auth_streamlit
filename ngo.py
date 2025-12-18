import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="NGO Management System",
    page_icon="🌱",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("vision", "Empowering lives through compassion.")
st.session_state.setdefault("mission", "Education, healthcare, and social welfare.")
st.session_state.setdefault("stats", {
    "Children Helped": "1200+",
    "Active Volunteers": "300+",
    "Ongoing Projects": "45+"
})
st.session_state.setdefault("initiatives", [
    "Free Education Program",
    "Women Empowerment",
    "Rural Health Support"
])

# ---------------- CSS ----------------
st.markdown("""
<style>
.header {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    color: #1e8449;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌍 NGO Panel")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Admin"]
)

# ================= HOME PAGE =================
if page == "Home":
    st.markdown('<div class="header">Helping Hands NGO</div>', unsafe_allow_html=True)
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🌟 Vision")
        st.write(st.session_state.vision)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 Mission")
        st.write(st.session_state.mission)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Impact Statistics")
    cols = st.columns(len(st.session_state.stats))
    for col, (k, v) in zip(cols, st.session_state.stats.items()):
        col.metric(k, v)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🚀 Our Initiatives")
    for item in st.session_state.initiatives:
        st.write("✔️", item)
    st.markdown('</div>', unsafe_allow_html=True)

    st.info("📩 Contact us at: support@helpinghands.org")

# ================= ADMIN PAGE =================
elif page == "Admin":
    st.markdown('<div class="header">Admin Dashboard</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Vision & Mission", "Statistics", "Initiatives"])

    # -------- TAB 1 --------
    with tabs[0]:
        st.subheader("Edit Vision & Mission")
        new_vision = st.text_area("Vision", st.session_state.vision)
        new_mission = st.text_area("Mission", st.session_state.mission)

        if st.button("Update"):
            st.session_state.vision = new_vision
            st.session_state.mission = new_mission
            st.success("Updated successfully")

    # -------- TAB 2 --------
    with tabs[1]:
        st.subheader("Manage Statistics")
        label = st.text_input("Statistic Name")
        value = st.text_input("Statistic Value")

        if st.button("Add / Update Statistic"):
            if label and value:
                st.session_state.stats[label] = value
                st.success("Statistic saved")

        st.write("### Current Statistics")
        st.write(st.session_state.stats)

    # -------- TAB 3 --------
    with tabs[2]:
        st.subheader("Manage Initiatives")
        initiative = st.text_input("New Initiative")

        if st.button("Add Initiative"):
            if initiative:
                st.session_state.initiatives.append(initiative)
                st.success("Initiative added")

        for i in st.session_state.initiatives:
            st.write("🔹", i)
