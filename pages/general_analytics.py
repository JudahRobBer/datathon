import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt





# functions to generate matplot tables
def make_language_chart(df:pd.DataFrame):
    pass

def make_focus_region_chart(df:pd.DataFrame):
    pass







    



def main():
    st.markdown("# General Analytics #")
    st.sidebar.markdown("# General Analytics #")
    
    df = pd.read_excel("CANIS_data.xlsx")
    
    
    #language_chart = make_language_pie_chart(df)
    #st.pyplot(language_chart)

main()