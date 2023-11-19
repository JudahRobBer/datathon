from dataclasses import dataclass
import pandas as pd
import numpy as np
import networkx as nx
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os
import random as rd
from bs4 import BeautifulSoup
from bs4.element import Comment
import pickle
import matplotlib.pyplot as plt
import pygraphviz


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
    time.sleep(rd.randrange(1,2))


def login_twitter(bot:webdriver.Chrome, email:str, username:str, password:str):
    """
    Login to twitter using selenium
    """

    bot.get('https://twitter.com/i/flow/login')
    # adjust the sleep time according to your internet speed
    
    #first login page
    sleep()
    username_button = bot.find_element(By.CSS_SELECTOR,"input[autocomplete= 'username']")
    sleep()
    username_button.click()
    
    username_box = bot.find_element(By.CSS_SELECTOR,"input[autocomplete= 'username']")
    sleep()
    username_box.send_keys(email)
    sleep()
    
    #click on button by text
    next_box = bot.find_element(By.XPATH,"//*[contains(text(),'Next')]")
    sleep()
    next_box.click()

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


def logout_twitter(bot:webdriver.Chrome):
    
    bot.get("https://twitter.com/logout")
    time.sleep(7)
    logout_button = bot.find_element(By.XPATH,"//*[contains(text(),'Log out')]")
    logout_button.click()


def add_account_followers_to_graph(bot:webdriver.Chrome,graph:nx.DiGraph):
    """
    after bot is logged into a given user
    check all the followers_you_follow page for the user account
    for each account, add the edges to the graph
    
    for account in acccount_handles:
        #get webpage
        #get followers data
        #add edges for each follower to account

    """
    def fake_movement(bot:webdriver.Chrome):
        bot.execute_script("window.scrollTo(0, document.body.scrollHeight);","")
        time.sleep(1)
        bot.execute_script("window.scrollBy(0, 0);","")

    print("getting followers")

    handles = list(graph.copy().nodes)
    handles = [handle for handle in handles if "attr" in graph.nodes[handle] and graph.nodes[handle]["attr"]["weight"] > 15000]
    size = len(handles)

    pause_intervals = set([size // 8,size // 6, size // 4, size // 3, size // 2, (size // 3) * 2, (size // 4) * 3, (size // 6) * 5])

    for index, account_handle in enumerate(handles):
        print(index)
        if index in pause_intervals:
            print("pausing to avoid suspicion!")
            fake_movement(bot)
            time.sleep(10)
        
       
        followers = []
        bot.get(f"https://twitter.com/{account_handle}/followers_you_follow")
        fake_movement(bot)
        time.sleep(rd.randrange(8,10))
        try:
            elements = bot.find_element(By.TAG_NAME, "section").get_attribute('innerHTML')
            soup = BeautifulSoup(elements, features="html.parser")
    
            data = soup.find_all("span", attrs={'class':"css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"})
            for element in data:
                if element.contents[0][0] == "@":
                    followers.append(element.contents[0][1:])
        except:
            pass
        
        for follower in followers:
            graph.add_edge(follower,account_handle)


   
    
def follow_all_accounts(bot:webdriver.Chrome,graph:nx.DiGraph, usernames:list, emails:list, password:str):
    """
    Before I'm able to check if a user follows another user,
    I first need to follow all the users in the dataset from controlled accounts
    With these accounts, I can find the accounts that follow the relevant account for check_followers
    
    """
    node_list = np.array_split(np.array(graph.nodes),10)

    for index,lst in enumerate(node_list):

        print(f"Starting list {index}")
        login_twitter(bot,emails[index],usernames[index],password)
        sleep()
        for index,node in enumerate(lst):
            print(node, index)
            bot.get(f"https://twitter.com/{node}")
            time.sleep(rd.randrange(2,5))
            try:
                follow_button = bot.find_element(By.XPATH,"//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div")
                follow_button.click()
            except:
                print("follow button not found")
            
            time.sleep(rd.randrange(2,5))
        print(f"list {index} complete! Taking a short break")
        
        #clean up cache and logout
        logout_twitter(bot)
        time.sleep(15)
    


def create_graph_edges(graph:nx.DiGraph) -> nx.DiGraph:
    """
    Iterate over the nodes in the graph, accessing their twitter handle to extract followers
    for every follower, if they are also a node, create an edge from them to account
    """
    
    bot = uc.Chrome()

    usernames = ["datacollec81608",
                 "datacollec51206",
                 "datacollec41168",
                 "datacollec74936",
                 "datacollec70650",
                 "datacollec68581",
                 "thesebitch99318",
                 "justonemor36852",
                 "finale699887",
                 "wemadeit578158"
                 ]
    emails = ["4bbdac6558e756@theeyeoftruth.com",
              "98915a6558e814@beaconmessenger.com",
              "06911d6558e877@theeyeoftruth.com", 
              "95d47b6558e8ef@beaconmessenger.com",
              "b151326558e975@theeyeoftruth.com",
              "0051cf6558e9dc@beaconmessenger.com",
              "4d63eb6558ea63@theeyeoftruth.com",
              "5f2e166558eced@beaconmessenger.com",
              "709d276559101d@beaconmessenger.com",
              "efd04f6558ee22@theeyeoftruth.com"]
    password = "testing12345"


    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/119.0.6045.169 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/119.0.6045.169 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPod; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/119.0.6045.169 Mobile/15E148 Safari/604.1",
    ]


    #this function has already been called during development. Calling it again is UB!
    #follow_all_accounts(bot,graph,usernames,emails,password)
    
    for i in range(len(usernames)):
        try:
            login_twitter(bot,emails[i],usernames[i],password)
            sleep()
            add_account_followers_to_graph(bot,graph)
            sleep()
            logout_twitter(bot)
            print(f"finished account {i + 1}")
        except:
            print(f"error with account {i + 1}")
            try:
                bot.close()
            except:
                pass
            bot = uc.Chrome()

        
        
    return graph



    
def create_graph_nodes(df:pd.DataFrame, graph:nx.DiGraph) -> nx.DiGraph:
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
    return graph
   



def create_graph() -> nx.DiGraph:
    """
    All commented out behavior cover functionality that only should be run once
    i.e: setting up follower accounts, following accounts, checking common followers
    writing graph edges and nodes.

    Now that all of this behavior is complete, this just serves to export the relevant graph
    
    """
    
    #df = load_data("CANIS_data.xlsx")
    
    #graph = create_graph_nodes(df,graph)
    #graph = create_graph_edges(graph)
    
    
    #pickle.dump(graph, open('graph.p','wb'))

    graph = pickle.load(open("graph.p","rb"))
    
    return graph

#create_graph()