import requests
import json
import pandas as pd
import streamlit as st
import plotly.express as px
#player_id = 13852993 #jochen
#player_id = 13766994 #adrian


# Get user input
player_id = st.text_input("Enter your AOE4 world string here, i.e. https://aoe4world.com/players/13766994 - the last string after 'players', "1270139")
st.write("The data is displayed for the player:", player_id)



def get_aoe4_data(player_id):
    result = requests.get(f'https://aoe4world.com/api/v0/players/{player_id}/games?leaderboard=rm_solo') 
    result = result.json()
    return result

def extract_game_date(result):
    games = result["games"]
    duration, server, maps = [], [], []

    for item in games:
        maps.append(item["map"])
        duration.append(item["duration"]/60)
        server.append(item["server"])

    return duration, server, maps

def define_dataframe(main_tuple):
    data_dict = {f'col{i}': lst for i, lst in enumerate(main_tuple)}
    df = pd.DataFrame(data_dict)
    df.columns = ['game_duration', 'server', 'map']
    return df


def main():

    result_main = get_aoe4_data(player_id)
    game_results_main = extract_game_date(result_main)
    df = define_dataframe(game_results_main)
    fig = px.scatter(df, x="server", y="game_duration", color = "map")
    st.plotly_chart(fig)


if __name__ == "__main__":
    df = main()

