import streamlit as st
import pandas as pd

def main():
    st.title("SMS Data Analysis")
    data = pd.read_csv("SMS_data.csv")

if __name__ == '__main__':
    main()