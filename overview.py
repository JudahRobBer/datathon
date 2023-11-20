import streamlit as st
import numpy as np
import pandas as pd



#import data as data frame


def main(): 
    st.markdown("# Introduction and Overview #")
    st.sidebar.markdown("# Introduction #")

    intro = """
    Foreign Interference is a developing issue facing democracy across the globe. Authoritarian regimes have leveraged the information networks of social media to influence and destabilize autonomous democracies. This issue spans Russian interference in US elections (Hosenball, 2020), the development of digital mobs in the Philippines (Ressa, 2023), the spread of climate denialism (Chavalarias et al., 2023), and the spread of Chinese propaganda networks.

    Through analyzing the collected dataset of known Chinese State Agents, I hope to gain insight into the behavior, spread, and strength of these networks.

    """

    intro_citation = """
        References: 
        
        Chavalarias, D., Bouchaud, P., Chomel, V., & Panahi, M. (2023). The new fronts of denialism and climate skepticism. 22–49. HAL Open Science. Hal-04103183
        
        Ressa, M. A. (2023). How to stand up to a dictator. WH Allen. 
        
        Hosenball, M. (2020, August 19). Factbox: Key findings from Senate inquiry into Russian interference in 2016 U.S. election. Reuters. https://www.reuters.com/article/us-usa-trump-russia-senate-findings-fact-idUSKCN25E2OY/

    """
    st.write(intro)
    st.caption(intro_citation)


main()
