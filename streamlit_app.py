import requests
import json
import pandas as pd
import streamlit as st
import plotly.express as px
#player_id = 13852993 #jochen
#player_id = 13766994 #adrian


player_id = int(st.text_input("Enter your AOE4 world string here, i.e. https://aoe4world.com/players/13766994 - the last string after players", "1270139"))
#st.write("You entered:", player_id)



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
    df_hero = df[df["profile_id"] == player_id]
    df_villain = df[df["profile_id"] != player_id]
    df_villain["opponent_civ"] = df["civilization"]
    villain_columns = ["opponent_civ", "game_id"]
    df_villain_info = df_villain[villain_columns]
    df_hero = df_hero.merge(df_villain_info, on='game_id', how='left')
    df_hero["duration"] = df_hero["duration"] / 60
    return df_hero

def interactive_plot(df):
    select_graph = ["scatter", "bar"]
    select_plot = st.selectbox("Select desired graph", select_graph)

    x_axis_val = st.selectbox("Select X-Axis Value", options=df.columns)
    y_axis_val = st.selectbox("Select Y-Axis Value", options=df.columns)
    color = st.selectbox("If you want to, select a column to color results", options=df.columns)
    
    
    if select_plot:
        plot_function = getattr(px, select_plot)
        
        fig = plot_function(df, x=x_axis_val, y=y_axis_val, color=color)
        
        st.plotly_chart(fig)
    else:
        st.write("Please select at least one plot type.")


def main ():
    
    result = get_aoe4_data(player_id)
    sublist = create_sublist(result)
    df = full_game_info_extractor(sublist)
    message = f'{player_id}, this resolves to the following playername: {df["name"].values[0]}'
    st.write("You entered:", message)
    st.dataframe(df.style.background_gradient(cmap='coolwarm'))
    interactive_plot(df)

if __name__ == "__main__":
    main()
