from googleapiclient.discovery import build
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


API_KEY = "AIzaSyBe82AdDqRnFR-L5WMO9HbVZ02l1iXOJI4"

youtube = build(
        serviceName='youtube',
        version='v3',
        developerKey=API_KEY
    )


def get_channel_id(username:str) -> str:
    
    request = youtube.channels().list(
        part= "id",
        forUsername = username
    )

    response = dict(request.execute())
    
    try:
        return response["items"][0]['id']
    except:
        return None


def get_channel_views(id:str):
    
    
    request = youtube.channels().list(
        part='statistics',
        id=id
    )
    response = dict(request.execute())

    try:
        views = int(response["items"][0]["statistics"]["viewCount"])
        return views
    except:
        return None

def get_channel_featured(id:str):
    request = youtube.channelSections().list(
        part = "contentDetails",
        channelId = id
    )

    response = dict(request.execute())
    try:
        return response['items'][-1]["contentDetails"]["channels"]
    except:
        return None


def get_channel_topicDetails(id:str):
    request = youtube.channels().list(
        part='topicDetails',
        id=id
    )
    response = dict(request.execute())
    try:
        return response["items"][0]["topicDetails"]["topicCategories"]
    except:
        pass


def get_valid_ids(df:pd.DataFrame, username_map:dict = None) -> list:
    """
    Only 15 of the 159 accounts seem to respond when I query with api
    just get these 15 accounts
    """
    account_names = df["YouTube account"].tolist()
    valid_ids= []
    found_names = set()
    account_urls = df["YouTube URL"]
    for account in account_urls:
        account = str(account)
        if account.find("channel") != -1:
            id = account[account.find("channel") + 8:]
            if id.find("/") != -1:
                id = id[:id.find("/")]
            
            if username_map is not None:
                row = df.loc[df['YouTube URL'] == account]
                youtube_account = row["YouTube account"]
                youtube_account = str(youtube_account).split(" ")[4]
                youtube_account = youtube_account[:youtube_account.find("\n")]
                
                #YunnanTV repeats
                if youtube_account not in found_names:
                    username_map[id] = youtube_account
                found_names.add(youtube_account)
            valid_ids.append(id)

    
    for name in account_names:
        id = get_channel_id(name)
        if id is None:
            id = get_channel_id("@" + name)
            print("needed to @")
        if id and id not in valid_ids and name not in found_names:
            valid_ids.append(name)
            if username_map is not None:
                row = df.loc[df['YouTube URL'] == name]
                youtube_account = row["YouTube account"]
                youtube_account = str(youtube_account).split(" ")[4]
                youtube_account = youtube_account[:youtube_account.find("\n")]
                if youtube_account not in found_names:
                    username_map[id] = youtube_account
                found_names.add(youtube_account)



    return valid_ids





def get_all_views_by_entity():
    df = pd.read_excel("CANIS_data.xlsx")
    user_id_map = {}
    
    entity_views = {}

    df = df.dropna(subset=["YouTube account"])
    valid_ids = get_valid_ids(df,user_id_map)
    
    #add following counts to parent entities counter
    for id in valid_ids:
        try:
            views = get_channel_views(id)
            
            row = df.loc[df['YouTube account'] == user_id_map[id]]
            parent_entity = str(row["Parent entity (English)"]).strip().split()
            end = parent_entity.index("Name:")
            parent_entity = " ".join(parent_entity[1:end])
            
            copy = ""
            for char in parent_entity:
                if char.isnumeric():
                    break
                copy += char
            parent_entity = copy
            
            
            if parent_entity in entity_views:
                entity_views[parent_entity] += views
            else:
                entity_views[parent_entity] = views
        except:
            pass
    
    
    tuple_list = []
    for key, value in entity_views.items():
        tuple_list.append((key,value))
    
    df = pd.DataFrame(tuple_list, columns=["Parent Entity", "Total Views"])
    df.to_csv("parent_youtube_views.csv")

def get_all_topics():
    """
    returns all the topics and their frequency

    """
    df = pd.read_excel("CANIS_data.xlsx")
    df = df.dropna(subset=["YouTube account"])
    valid_ids = get_valid_ids(df)

    
    topic_counts = {}

    for id in valid_ids:
        try:
            topics = get_channel_topicDetails(id)
            
            if topics:
                for topic in topics:
                    topic = topic[topic.rfind("/") + 1:]
                    if topic in topic_counts:
                        topic_counts[topic] += 1
                    else:
                        topic_counts[topic] = 1
        except:
            pass
    
    tuple_list = []
    for key, value in topic_counts.items():
        tuple_list.append((key,value))
    
    
    df = pd.DataFrame(tuple_list, columns=["Topic", "Frequency"])
    df.to_csv("topic_frequency.csv")
    

    






    
