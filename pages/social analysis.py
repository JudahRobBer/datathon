import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
from graph import create_graph
import networkx as nx
import random as rd
from wordcloud import WordCloud
from scipy import stats
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
    
    def set_node_sizes(graph) -> list:
        node_sizes = []
        max_weight = 0
        for node,attr in graph.copy().nodes(data= True):
            try:
                cur = attr["attr"]["weight"]
                if cur > max_weight:
                    max_weight = cur
            except:
                print("failed")
                graph.remove_node(node)
                pass
        

        #size nodes
        #using the max weight, normalize the values and scale by 100
        for node, attr in graph.nodes(data=True):
            node_sizes.append((attr["attr"]["weight"] / max_weight) * 700)
        return node_sizes
    
    def set_node_colors(graph):
        #color by Entity Owner
        hex_colors = ["#{:06x}".format(rd.randint(0, 0xFFFFFF)) for _ in range(100)]
        color_map = {}
        color_list = []
        counter = 0
        for node, attr in graph.nodes(data=True):
            
            try:
                entity = attr["attr"]["entity"]
                print(entity)
                if entity not in color_map:
                    color = rd.choice(hex_colors)
                    color_map[entity] = color
                    hex_colors.remove(color)
                color_list.append(color_map[entity])
            except:
                counter += 1
                color_list.append(hex_colors[0])
        print(counter)
        return color_list
    
    
    outdeg = list(graph.out_degree())
    indeg = list(graph.in_degree())
    filtered = [outdeg[n][0] for n in range(len(outdeg)) if outdeg[n][1] > 0 or indeg[n][1] > 0]

    subgraph = graph.subgraph(filtered).copy()
    sub_node_sizes = set_node_sizes(subgraph)
    sub_color_list = set_node_colors(subgraph)
    
   
    graph_caption = """
    Directed Graph displaying follower relationship within the state agent dataset.
    Accounts with less than 1500 followers were excluded from following analysis.
    Nodes are color coded by Entity Owner, and sized twitter follower count
    """

    junction_caption = """
        A junction tree is created with the following steps: 
        1) Moralize, Triangulate, find maximul cliques
        2) build tree by connecting cliques with shared nodes
        3) find the maximal spanning tree
       
    """
    junction_function = """
     A junction tree serves to reduce the visual complexity of the graph
        while providing insight into community formation.
    """
   
    junction = nx.junction_tree(subgraph).copy()
   

    fig, ax = plt.subplots()
    nx.draw(subgraph,node_size=sub_node_sizes, node_color=sub_color_list,width=.05)
    st.pyplot(fig)
    st.caption(graph_caption)
    
    st.write("Junction Tree: ")
    
    fig, ax = plt.subplots()
    pos = nx.nx_agraph.graphviz_layout(junction)
    nx.draw(junction,node_size = 25, pos=pos)
    st.pyplot(fig)
    st.caption(junction_caption)
    st.caption(junction_function)




def make_pagerank_table(graph:nx.DiGraph):
    pagerank = nx.pagerank(graph)
    
    sorted_pagerank = sorted(pagerank.items(),key= lambda x: x[1], reverse=True)
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
    

def make_page_rank_twitter_follower_scatter(graph:nx.DiGraph,df:pd.DataFrame):
    #scatter the page ranks of accounts with > 15000 followers against follower count
    column_label = "X (Twitter) handle"
    df = df.dropna(subset=[column_label])
    pagerank = nx.pagerank(graph)
    follower_pagerank_map = {}

    for handle, rank in pagerank.items():
        row = df.loc[df[column_label] == handle]
        followers = list(row["X (Twitter) Follower #"])
        if followers:
            followers = followers[0]
            if followers > 15000:
                follower_pagerank_map[followers] = float(rank)

    lst = list(follower_pagerank_map.items())
    df = pd.DataFrame(lst,columns=["Followers","Page Rank"])
    followers = df["Followers"].tolist()
    ranks = df["Page Rank"].tolist()
    r_value = stats.pearsonr(followers,ranks)[0]
    fig, ax = plt.subplots()
    ax.set_xlabel("Twitter Followers (log)")
    ax.set_ylabel("Page Rank")
    ax.set_title("Page Rank vs Twitter Followers Plot")
    
    scatter = plt.scatter(followers,ranks)
    
    ax.set_xscale("log")
    
    st.pyplot(fig)
    st.caption(f"R-Value: {r_value}")



    #get the page ranks for these handles

     
def make_facebook_follower_swarm(df:pd.DataFrame):
    fb_frame = df.dropna(subset=["Facebook page"])
    fb_frame = fb_frame[["Facebook Follower #", "Language"]]
    
    #get 5 most common languages
    counts = {}
    for index, row in fb_frame.iterrows():
        lang = row["Language"]
        if lang in counts:
            counts[lang] += 1
        else:
            counts[lang] = 1
    
    most_common_langs = sorted(counts.items(), key= lambda x:x[1], reverse=True)
    top_5 = set([lang[0] for lang in most_common_langs[:5]])

    
    fb_frame = fb_frame[fb_frame["Language"].isin(top_5)]
    sns.set(style="whitegrid")
    
    
    fig, ax = plt.subplots()
    ax.set_yscale("log") # log first
    swarm = sns.swarmplot(x = "Language", y="Facebook Follower #", data=fb_frame)
    
    st.pyplot(fig)


def make_facebook_follower_bar(df:pd.DataFrame):
    fb_frame = df.dropna(subset=["Facebook page"])
    fb_frame = fb_frame[["Facebook Follower #", "Region of Focus"]]

    #display 5 regins with most followers
    regions = {}
    for index, row in fb_frame.iterrows():
        region = row["Region of Focus"]
        followers = row["Facebook Follower #"]
        if region in regions:
            regions[region] += followers
        else:
            regions[region] = followers
    
    most_followed_regions = sorted(regions.items(), key= lambda x:x[1], reverse=True)
    top_5 = [region for region in most_followed_regions[:5]]
    df = pd.DataFrame(top_5, columns = ["Region", "Followers"])
    
    st.bar_chart(x="Region",y="Followers",data=df)


def make_youtube_parent_views_bubble():
    df = pd.read_csv("parent_youtube_views.csv")
    labels = df["Parent Entity"].tolist()
    views = df["Total Views"].tolist()
    
    fig, ax = plt.subplots()
    ax.set_yscale("log") # log first
    #ax.set_xticks(views,labels, rotation=45, ha='right')
   
    bar = plt.bar(x=labels,height =views)
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    
    st.pyplot(fig)


def make_youtube_topic_frequency_cloud():
    df = pd.read_csv("topic_frequency.csv")
    cloud_str = ""
    for index, row in df.iterrows():
        topic = str(row["Topic"])
        if topic == "Lifestyle_(sociology)":
            topic = "Lifestyle"
        frequency = int(row["Frequency"])
        
        cloud_str += ((topic + " ") * frequency)
    fig, ax = plt.subplots()
    wordcloud = WordCloud(width=480, height=480, margin=0,collocations = False).generate_from_text(cloud_str)
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis("off")
    st.pyplot(fig)


def main():
    st.markdown("# Social Media Analysis #")
    st.sidebar.markdown("# Social Media Analysis #")
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

    youtube_caption = """
    Unfortunately, of the 159 valid youtube accounts, 
    through accessing both the URL's and given handles, I was only able to get 79
    accounts that would return information in youtube's API.

    I have yet to diagnose the cause of this limitation.

    """


    with overview:
        st.header("Social Media Overview")
        st.write(overview_motivation)
        st.write(overview_invest)
        fig1 = make_social_ven_diagram(df)
        st.pyplot(fig1)
        st.caption("Ven Diagram of account ownership")
    with twitter:
        st.header("Twitter Analysis")
        st.write("Follower Network:")
        make_twitter_network(graph)
    
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

        make_page_rank_twitter_follower_scatter(graph,df)

    with facebook:
        st.header("Facebook Analysis")
        
        st.write("Grouped Follower Swarm: ")
        make_facebook_follower_swarm(df)

        st.write("Total Followers by Region: ")
        make_facebook_follower_bar(df)
    with youtube:
        st.header("Youtube Analysis")
        st.write(youtube_caption)
        make_youtube_topic_frequency_cloud()
        st.caption("Word Cloud of youtube channel topics")
        st.write("Youtube Total View Data by Parent Entity")
        make_youtube_parent_views_bubble()

main()