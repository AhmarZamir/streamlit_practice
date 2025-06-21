from bs4 import BeautifulSoup
import requests
import streamlit as st
import re 

# Add headers to prevent blocking
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    data = requests.get("http://api.scraperapi.com", params={
    'api_key': st.secrets["SCRAPER_API_KEY"],
    'url': 'https://www.cricbuzz.com/'
})

    data.raise_for_status()  # Check for request errors
    soup = BeautifulSoup(data.text, 'html.parser')
except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()  # Stop if we can't get data

st.title("CricBuzz")
st.header("Live Cricket Score")

match_sections = soup.find_all('li',class_="cb-view-all-ga cb-match-card cb-bg-white")

for section in match_sections:
    title = section.find("div",class_="cb-col-90 cb-color-light-sec cb-ovr-flo")
    
    teams = section.find_all("div",class_="cb-col-50 cb-ovr-flo cb-hmscg-tm-name")
    
    score1 = section.find_all("div",class_="cb-hmscg-tm-bat-scr cb-font-14")
    score2 = section.find_all("div","cb-hmscg-tm-bwl-scr cb-font-14")
    
    status = section.find("div",class_="cb-mtch-crd-state cb-ovr-flo cb-font-12 cb-text-complete")
    status2 = section.find("div",class_="cb-mtch-crd-state cb-ovr-flo cb-font-12 cb-text-apple-red")
    status3 = section.find("div",class_="cb-ovr-flo cb-mtch-crd-time cb-font-12 cb-text-preview ng-binding ng-scope")

    st.subheader(title.text.strip() if title else "Match")

    for i in range(len(teams)):
        if i<len(score1):
            if(score1):
               format = re.sub(r'(\D+)(\d)', r'\1    \2', score1[i].text.strip())
               st.write(format)
            else: st.write("NA")
       
        if i<len(score2):
            if score2:
               format = re.sub(r'(\D+)(\d)', r'\1    \2', score2[i].text.strip())
               st.write(format)
            else: st.write("NA")

    if status:
        st.write(f"Status: {status.text.strip()}")
    elif status2:
        st.write(f"Status: {status2.text.strip()}")
    elif status3:
        st.write(f"Status: {status3.text.strip()}")
    else:
        st.write("Status: Upcoming Mathes")