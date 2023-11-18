import streamlit as st
import numpy as np
import pandas as pd



#import data as data frame


def main(): 
    df = pd.read_excel("CANIS_DATA.xlsx")
    df = df.dropna(subset="X (Twitter) handle")
    print(df.loc[:,"X (Twitter) handle"])


main()
