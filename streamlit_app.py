import requests
import json
import pandas as pd
import plotly.express as px
player_id = 13852993 #jochen
#player_id = 13766994 #adrian




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

def full_game_info_extractor(sublist):
    game_data = {}     
    for item in sublist:
        game_id = item["game_id"]
        maps = item["map"]
        server = item["server"]
        duration = item["duration"]

        if item["teams"][0][0]["player"]["profile_id"] == player_id:
            hero = item["teams"][0][0]["player"]["profile_id"]
            result_hero = item["teams"][0][0]["player"]["result"]
            mmr_diff_hero = item["teams"][0][0]["player"]["mmr_diff"]
            civ_hero = item["teams"][1][0]["player"]["civilization"]
            civ_opponent = item["teams"][1][0]["player"]["civilization"]

        if  item["teams"][1][0]["player"]["profile_id"] == player_id:
            hero = item["teams"][0][0]["player"]["profile_id"]
            result_hero = item["teams"][0][0]["player"]["result"]
            mmr_diff_hero = item["teams"][0][0]["player"]["mmr_diff"]
            civ_hero = item["teams"][1][0]["player"]["civilization"]

        game_data[game_id] = {
            "maps" : maps,
            "server": server,
            "duration": duration/60,
            "hero": hero,
            "result_hero": result_hero,
            "mmr_diff_hero": mmr_diff_hero,
            "civ_hero": civ_hero,
            "civ_opponent": civ_opponent
        }     
        df = pd.DataFrame(game_data).T
    return df



def main():

    result = get_aoe4_data(player_id)
    #print(result_main)
    #game_results_main = extract_game_date(result_main)
    #df = define_dataframe(game_results_main)
    #fig = px.scatter(df, x="server", y="game_duration", color = "map")
    #st.plotly_chart(fig)
    
    sublist = create_sublist(result)
    df = full_game_info_extractor(sublist)
    fig = px.scatter(df, x="civ_opponent", y="duration", color = "result_hero")
    #fig.show()

    st.plotly_chart(fig)
    return df



if __name__ == "__main__":
   df = main()

