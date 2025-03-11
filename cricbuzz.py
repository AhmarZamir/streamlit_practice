import streamlit as st

from bs4 import BeautifulSoup
import requests
import streamlit as st

data = requests.get("https://www.cricbuzz.com/")

soup = BeautifulSoup(data.text, 'html.parser')


# match_title =soup.find_all('div', class_="cb-col-90 cb-color-light-sec cb-ovr-flo")
# score_card = soup.find_all('li', class_="cb-view-all-ga cb-match-card cb-bg-white")


st.title("CricBuzz")
st.header("live Cricket Score")


match_sections = soup.find_all('li',class_="cb-view-all-ga cb-match-card cb-bg-white")





for  section in match_sections:
    # st.write(section.text)
    title = section.find("div",class_="cb-col-90 cb-color-light-sec cb-ovr-flo")
    teams = section.find_all("span",class_="text-normal")
    scores = section.find_all("div",class_="cb-ovr-flo")
   
    # team2 = section.find("span",class_="text-normal")



    st.subheader(title.text.strip())

    for i in range(len(teams)):
       team_name = teams[i-1].text.strip()
       team_score = scores[i-1].text.strip()
       st.write(f"{team_name}   vs   {team_score}")



    #  completed
    #   succesfully