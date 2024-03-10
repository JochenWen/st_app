import requests
import json
import pandas as pd
import streamlit as st
import plotly.express as px
player_id = 13852993 #jochen
#player_id = 13766994 #adrian
#player_id = st.text_input("Enter your AOE4 world string here, i.e. https://aoe4world.com/players/13766994 - the last string after players", "1270139")

def get_aoe4_data(player_id):
    try:
        result = requests.get(f'https://aoe4world.com/api/v0/players/{player_id}/games?leaderboard=rm_solo') 
        result = result.json()
    except:
        result = "player_string doesn't exist"
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

def create_sublist(result):
    sublist = []
    for item in result["games"]:
        sublist.append(item)
    return sublist

def full_game_info_extractor(data):
    data_output = []

    for item in data:
        data_output.append(item)



    unnested_data = []
    for game in data_output:
        for team in game['teams']:
            for player_info in team:
                game_info = game.copy()
                game_info.update(player_info['player'])
                del game_info['teams']
                unnested_data.append(game_info)

    df = pd.DataFrame(unnested_data)
    df["duration"] = df["duration"]/60
    df_hero = df[df["profile_id"] == player_id]
    df_villain = df[df["profile_id"] != player_id]
    df_villain["opponent_civ"] = df["civilization"]
    villain_columns = ["opponent_civ", "game_id"]
    df_villain_info = df_villain[villain_columns]
    df_hero = df_hero.merge(df_villain_info, on='game_id', how='left')
    return df_hero



#player_id = st.text_input("Enter your AOE4 world string here, i.e. https://aoe4world.com/players/13766994 - the last string after players", "1270139")


result = get_aoe4_data(player_id)
    #print(result_main)
    #game_results_main = extract_game_date(result_main)
    #df = define_dataframe(game_results_main)
    #fig = px.scatter(df, x="server", y="game_duration", color = "map")
    #st.plotly_chart(fig)

sublist = create_sublist(result)
df = full_game_info_extractor(sublist)


#print(df)
fig = px.scatter(df, x="opponent_civ", y="duration", color = "result")
#fig.show()
st.line_chart(df, x="started_at", y="rating")

st.dataframe(df.style.highlight_max(axis=0))
st.plotly_chart(fig)

