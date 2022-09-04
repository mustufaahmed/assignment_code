import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# return spam data and input dataframe
def getSpamData(data):
    return data[data['Label'] == 'Spam']

# return non-spam data and input dataframe
def getNotSpamData(data):
    return data[data['Label'] == 'Non-Spam']

def getBarChartPlot(data,color="blue"):
    monthly_count = data.groupby('Month')['Message_body'].count().sort_values(ascending=True)
    fig = plt.figure(figsize=(18,5), dpi=100)
    plt.bar(monthly_count.index, height=monthly_count.values,color=color)
    st.pyplot(fig)

def main():
    st.title("SMS Data Analysis")
    data = pd.read_csv("SMS_data.csv",encoding='unicode_escape')
    data['Date_Received'] = pd.to_datetime(data['Date_Received'])
    # create a new column of month
    data['Month'] = data['Date_Received'].apply(lambda x: x.month_name())
    
    # Get Data Where Only Spam Messages
    spam_messages = getSpamData(data)
    # Get Frequency of spam messages according to months
    st.header("Frequency Of Spam Messages")
    getBarChartPlot(spam_messages)

    # Get Data Where Only Non Spam Messages
    non_spam_messages = getSpamData(data)
    # Get Frequency of non spam messages according to months
    st.header("Frequency Of Non Spam Messages")
    getBarChartPlot(non_spam_messages,"red")


if __name__ == '__main__':
    main()