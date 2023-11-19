import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
from graph import create_graph
import networkx as nx
import random as rd
import itertools




def make_social_ven_diagram(df:pd.DataFrame):
    """
    Create ven diagram from sets
    """
    twt = "X (Twitter) handle"
    fb = "Facebook page"
    yt = "YouTube account"
    fb_frame = df.dropna(subset=[fb])
    twt_frame = df.dropna(subset=[twt])
    yt_frame = df.dropna(subset=[yt])


    key = "Name (English)"
    #individuals:
    fb_set = set()
    for index, row in fb_frame.iterrows():
        fb_set.add(row[key])

    twt_set = set()
    for index, row in twt_frame.iterrows():
        twt_set.add(row[key])

    yt_set = set()
    for index, row in yt_frame.iterrows():
        yt_set.add(row[key])

    
    fig, ax = plt.subplots(figsize=(7,5))

    v = venn3([yt_set,twt_set,fb_set],set_labels=("Youtube","Twitter","Facebook"),ax=ax)
    return fig


def make_twitter_network(graph:nx.DiGraph):
    
    node_sizes = []
    max_weight = 0
    for node,attr in graph.copy().nodes(data= True):
        try:
            cur =  attr["attr"]["weight"]
            if cur > max_weight:
                max_weight = cur
        except:
            graph.remove_node(node)
    #size nodes
    #using the max weight, normalize the values and scale by 100
    for node, attr in graph.nodes(data=True):
        node_sizes.append((attr["attr"]["weight"] / max_weight) * 600)
    
    #color by Entity Owner
    hex_colors = ["#{:06x}".format(rd.randint(0, 0xFFFFFF)) for _ in range(100)]
    color_map = {}
    color_list = []
    for node, attr in graph.nodes(data=True):
        entity = attr["attr"]["entity"]
        if entity not in color_map:
            color = rd.choice(hex_colors)
            color_map[entity] = color
            hex_colors.remove(color)
        color_list.append(color_map[entity])
    
    
    fig, ax = plt.subplots()
    nx.draw(graph,node_size=node_sizes, node_color=color_list,width=.05)
    return fig


def make_pagerank_table(graph:nx.DiGraph):
    pagerank = nx.pagerank(graph)
    #print(pagerank)
    sorted_pagerank = sorted(pagerank.items(),key= lambda x: x[1], reverse=True)
    print(sorted_pagerank)
    df = pd.DataFrame(sorted_pagerank[:10], columns = ["Twitter Handle","Page Rank"])
    st.dataframe(df)


def make_betweenness_table(graph:nx.DiGraph):
    betweenness = nx.betweenness_centrality(graph)
    sorted_betweenness = sorted(betweenness.items(),key= lambda x: x[1], reverse=True)
    df = pd.DataFrame(sorted_betweenness[:10], columns = ["Twitter Handle","Betweenness \n Centrality"])
    st.dataframe(df)


def make_out_degree_table(graph:nx.DiGraph):
    out_degree = dict(graph.out_degree())
    sorted_out_degree = sorted(out_degree.items(),key= lambda x: x[1], reverse=True)
    df = pd.DataFrame(sorted_out_degree[:10], columns = ["Twitter Handle","Out Degree"])
    st.dataframe(df)


def make_in_degree_table(graph:nx.DiGraph):
    in_degree = dict(graph.in_degree())
    sorted_in_degree = sorted(in_degree.items(),key= lambda x: x[1], reverse=True)
    df = pd.DataFrame(sorted_in_degree[:10], columns = ["Twitter Handle","In Degree"])
    st.dataframe(df)

     


def make_twitter_follower_hist(df:pd.DataFrame):
    pass




def make_facebook_follower_density(df:pd.DataFrame):
    pass


def make_youtube_subscriber_bubble(df:pd.DataFrame):
    pass


def main():
    st.markdown("# Social Media Analytics #")
    st.sidebar.markdown("# Social Media Analytics #")
    overview,twitter, facebook, youtube = st.tabs(["Overview","Twitter","Facebook","Youtube"])
    df = pd.read_excel("CANIS_data.xlsx")
    graph = create_graph()
    overview_motivation = """
    Motivation:

	Analysis of social media presence allows a better understanding of both the 
    overall spread of state influence as well as the relationships formed by 
    state agents within broader informational ecosystems.

    """
    overview_invest = """
    Investigation:
	
	I relied on twitter follower/following relationships 
    within the data set to create a relational understanding 
    of the state agents and Facebook followers / Youtube total channel views 
    to effectively convey the total reach of the state agents.
    """
    
    graph_caption = """
    Directed Graph displaying follower relationship within the state agent dataset.
    Accounts with less than 1500 followers were excluded from following analysis.
    Nodes are color coded by Entity Owner, and sized twitter follower count
    """

    centrality_caption = """
    Source: https://cambridge-intelligence.com/keylines-faqs-social-network-analysis/

    Page Rank informs us of the accounts with the most influence within the network. 
    Betweenness centrality provides shows the nodes that act as bridges within the network

    """

    degree_caption = """
    In addition to more complex analysis, in and out degree provide valuable insight
    into the most involved members of a network. As an extension, checking a new nodes
    out degree would provide information about their level of consumption of the content in the network
    """


    with overview:
        st.header("Social Media Overview")
        st.write(overview_motivation)
        st.write(overview_invest)
        fig1 = make_social_ven_diagram(df)
        st.pyplot(fig1)
    with twitter:
        st.header("Twitter Analysis")
        st.write("Follower Network:")
        fig = make_twitter_network(graph)
        st.pyplot(fig)
        st.caption(graph_caption)
        st.write("Network Analysis:")
        col1, col2 = st.columns(2)
        with col1:
            make_pagerank_table(graph)
        with col2:
            make_betweenness_table(graph)

        st.caption(centrality_caption)

        col3, col4 = st.columns(2)
        with col3:
            make_out_degree_table(graph)
        with col4:
            make_in_degree_table(graph)
        st.caption(degree_caption)

    with facebook:
        st.header("Facebook Analysis")
    with youtube:
        st.header("Youtube Analysis")

main()