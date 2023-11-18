from dataclasses import dataclass
import pandas as pd
import numpy as np
import streamlit as st
import networkx as nx
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os
import random as rd


"""
    Generate network of members of the data set with a twitter account.
    Represent the network as a directed graph of members of the data set.
    Each Node Weight is determined by the total number of followers
    Every directed edge represents a follower relationship

"""


@dataclass
class Node:
    """
    Data class to store information about a node, translated to a dictionary before use
    """
    weight:int = None
    name:str = None
    language:str = None
    entity:str = None
    region:str = None


def load_data(filename:str) -> pd.DataFrame:
    df = pd.read_excel(filename)
    df = df.dropna(subset="X (Twitter) handle")
    return df


def sleep():
    time.sleep(rd.randrange(1,4))


def login_twitter(bot:webdriver.Chrome):
    """
    Login to twitter using selenium
    """
    email = "jrobbinsbernal@colgate.edu"
    password = "Jewdah17!"
    username = "judahlovesdata"

    bot.get('https://twitter.com/i/flow/login')
    # adjust the sleep time according to your internet speed
    
    #first login page
    sleep()
    bot.find_element(By.CSS_SELECTOR,"input[autocomplete= 'username']").click()
    sleep()
    
    bot.find_element(By.CSS_SELECTOR,"input[autocomplete= 'username']").send_keys(email)
    sleep()
    
    #click on button by text
    bot.find_element(By.XPATH,"//*[contains(text(),'Next')]").click()

    sleep()

    def password_page(bot:webdriver.Chrome,password:str):
        bot.find_element(By.CSS_SELECTOR,"input[name= 'password']").send_keys(password)
        sleep()
        bot.find_element(By.CSS_SELECTOR,"input[name= 'password']").send_keys(Keys.RETURN)
        
       

    try:
        password_page(bot,password)
    except: #redirected to fishy login page
        sleep()

        bot.find_element(By.TAG_NAME,"input").send_keys(username)
        sleep()
        bot.find_element(By.XPATH,"//*[contains(text(),'Next')]").click()
        sleep()
        password_page(bot,password)
        sleep()


def navigate_search(bot:webdriver.Chrome,twitter_handle:str):
    sleep()
    bot.get("https://twitter.com/explore")
    sleep()
    search_bar =  bot.find_element(By.TAG_NAME,"input")
    search_bar.click()
    search_bar.send_keys(twitter_handle)
    search_bar.send_keys(Keys.RETURN)
    

    


def get_twitter_followers(twitter_handle:str) -> list[str]: 
   
    
    email = "jrobbinsbernal@colgate.edu"
    password = "Jewdah17!"
    username = "judahlovesdata"
    
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("window-size=1200x600")
    # Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
 
    # Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False) 

    
    bot = webdriver.Chrome(options=options)

    login_twitter(bot)
    navigate_search(bot,twitter_handle)
    time.sleep(15)
    
    
   



def create_graph_edges(graph:nx.DiGraph) -> None:
    """
    Iterate over the nodes in the graph, accessing their twitter handle to extract followers
    for every follower, if they are also a node, create an edge from them to account
    """
    
   
    
    #set to improve search efficiency
    node_set = set()
    for node in graph.nodes:
        node_set.add(node)
    
    users = list(graph.nodes)
    print(len(users))
    


    


def create_graph_nodes(df:pd.DataFrame, graph:nx.DiGraph) -> None:
    """
    load in the dataframe including only entries with twitter handles
    iterate over handles in the data frame, add them as nodes with relevant information
    """
  

    for index, row in df.iterrows():
        wght = int(row["X (Twitter) Follower #"])
        nme = row["Name (English)"]
        lngge = row["Language"]
        rgn = row["Region of Focus"]
        entty = row["Entity owner (English)"]
        
        node = Node(weight=wght, name = nme, language = lngge, region = rgn, entity = entty)
        node_id = row["X (Twitter) handle"]
        
        node_dict = vars(node)
        graph.add_node(node_id,attr=node_dict)
   



def create_graph() -> nx.DiGraph:
    df = load_data("CANIS_data.xlsx")
    graph = nx.DiGraph()
    create_graph_nodes(df,graph)
    #create_graph_edges(graph)
    get_twitter_followers("_bubblyabby_")

create_graph()