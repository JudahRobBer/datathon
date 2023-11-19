import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2,venn3



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




    
    
    pass


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

    with overview:
        st.header("Social Media Overview")
        st.write("Social Media offers States and State Offiliated media ")
        fig1 = make_social_ven_diagram(df)
        st.pyplot(fig1)
    with twitter:
        st.header("Twitter analysis")
    with facebook:
        st.header("Facebook Analysis")
    with youtube:
        st.header("Youtube Analysis")

main()