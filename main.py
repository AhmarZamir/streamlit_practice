from bs4 import BeautifulSoup
import requests
import streamlit as st
import re

# Initialize session state for theme if not already set
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark Mode" # Default theme

# Sidebar
with st.sidebar:
    st.markdown(
        '<h1 style="text-align:center; color:#016080; font-family:sans-serif; height:70px; width:200px; font-size:40px;">CricBuzz</h1>',
        unsafe_allow_html=True
    )
    st.divider()
    select_status = st.selectbox("Filter by Status", ["All", "Featured", "Result"])
    st.divider()
    select_format = st.selectbox("Filter by Format", ["All", "Test", "ODI", "T20"])
    st.divider()

    # Use a key to update session state when the selectbox changes
    selected_mode = st.selectbox("Theme", ["Dark Mode", "Light Mode"], key="theme_selector")
    if selected_mode != st.session_state.theme_mode:
        st.session_state.theme_mode = selected_mode
        st.rerun() # Rerun to apply theme changes immediately

# Define colors based on session state theme
if st.session_state.theme_mode == "Light Mode":
    st.markdown("""
    <style>
        /* Whole Page Background */
        [data-testid="stAppViewContainer"] {
            background-color: #E0E0E0;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #1F1F1F;
            border-right: 2px solid #bbb;
        }
    </style>
    """, unsafe_allow_html=True)
    font_color = "#016080"
    status_color = "#016080"
else: 
    font_color = "#016080"
    status_color = "#016080"

# The rest of your code remains largely the same...

# Header
st.markdown(
    '<h1 style="text-align:center; color:#016080; font-family:sans-serif;">Live Cricket Score</h1>',
    unsafe_allow_html=True
)
st.divider()

# Fetch HTML
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

try:
    data = requests.get("http://api.scraperapi.com", params={
        'api_key': st.secrets["SCRAPER_API_KEY"],
        'url': 'https://www.cricbuzz.com/'
    }, headers=headers)

    data.raise_for_status()
    soup = BeautifulSoup(data.text, 'html.parser')
except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

# Parse matches
match_sections = soup.find_all('li', class_="cb-view-all-ga cb-match-card cb-bg-white")

for section in match_sections:
    title = section.find("div", class_="cb-col-90 cb-color-light-sec cb-ovr-flo")
    teams = section.find_all("div", class_="cb-col-50 cb-ovr-flo cb-hmscg-tm-name")
    score1 = section.find_all("div", class_="cb-hmscg-tm-bat-scr cb-font-14")
    score2 = section.find_all("div", class_="cb-hmscg-tm-bwl-scr cb-font-14")

    status = section.find("div", class_="cb-mtch-crd-state cb-ovr-flo cb-font-12 cb-text-complete")
    status2 = section.find("div", class_="cb-mtch-crd-state cb-ovr-flo cb-font-12 cb-text-apple-red")
    status3 = section.find("div", class_="cb-ovr-flo cb-mtch-crd-time cb-font-12 cb-text-preview ng-binding ng-scope")

    test = section.find("div",class_="cb-card-match-format text-center text-white cb-tst-tg-wdt-34 cb-mtch-frmt-bg-test-red")
    t20 = section.find("div", class_="cb-card-match-format text-center text-white cb-mtch-frmt-bg-t20")

    is_result = status or status2
    is_featured = not is_result

    format_div = section.find("div", class_=re.compile("cb-card-match-format"))
    match_format = None
    if format_div:
        format_classes = format_div.get("class", [])
        if "cb-mtch-frmt-bg-test-red" in format_classes:
            match_format = "Test"
        elif "cb-mtch-frmt-bg-t20" in format_classes:
            match_format = "T20"
        elif "cb-mtch-frmt-bg-odi" in format_classes:
            match_format = "ODI"

    is_result = bool(status or status2)
    is_featured = not is_result

    format_match = (
        select_format == "All" or
        (select_format == "Test" and match_format == "Test") or
        (select_format == "ODI" and match_format == "ODI") or
        (select_format == "T20" and match_format == "T20")
    )

    status_match = (
        select_status == "All" or
        (select_status == "Result" and is_result) or
        (select_status == "Featured" and is_featured)
    )

    if format_match and status_match:
        if(title):
            st.markdown(
                f'<h2 style=" color:{font_color}; font-family:sans-serif; font-size:18px;"> {title.text.strip()}    ({match_format})</h2>',
                unsafe_allow_html=True
            )

        for i in range(len(teams)):
            if i < len(score1):
                if(score1):
                    format = re.sub(r'(\D+)(\d)', r'\1    \2', score1[i].text.strip())
                    st.markdown(
                        f'<h1 style=" color:{font_color}; font-family:sans-serif; font-size:18px;">{format}</h1>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<h1 style=" color:{font_color}; font-family:sans-serif; font-size:18px;">NA</h1>',
                        unsafe_allow_html=True
                    )
            if i < len(score2):
                if score2:
                    format = re.sub(r'(\D+)(\d)', r'\1    \2', score2[i].text.strip())
                    st.markdown(
                        f'<h1 style=" color:{font_color}; font-family:sans-serif; font-size:18px;"> {format}</h1>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<h1 style=" color:{font_color}; font-family:sans-serif; font-size:18px;">NA</h1>',
                        unsafe_allow_html=True
                    )

        if status:
            st.markdown(
                f'<h1 style=" color:{status_color}; font-family:sans-serif; font-size:18px;">Status: {status.text.strip()}</h1>',
                unsafe_allow_html=True
            )
        elif status2:
            st.markdown(
                f'<h1 style=" color:{status_color}; font-family:sans-serif; font-size:18px;">Status: {status2.text.strip()}</h1>',
                unsafe_allow_html=True
            )
        elif status3:
            st.markdown(
                f'<h1 style=" color:{status_color}; font-family:sans-serif; font-size:18px;">Status: {status3.text.strip()}</h1>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<h1 style=" color:{status_color}; font-family:sans-serif; font-size:18px;">Status: Upcoming Matches</h1>',
                unsafe_allow_html=True
            )
        st.divider()