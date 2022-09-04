import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# return spam data and input dataframe
def getSpamData(data):
    return data[data['Label'] == 'Spam']

# return non-spam data and input dataframe
def getNotSpamData(data):
    return data[data['Label'] == 'Non-Spam']

def getBarChartPlot(data):
    monthly_count = data.groupby('Month')['Message_body'].count().sort_values(ascending=True)
    plt.figure(figsize=(18,5), dpi=100)
    plt.bar(monthly_count.index, height=monthly_count.values)


def main():
    st.title("SMS Data Analysis")
    data = pd.read_csv("SMS_data.csv",encoding='unicode_escape')
    data['Date_Received'] = pd.to_datetime(data['Date_Received'])
    # create a new column of month
    data['Month'] = data['Date_Received'].apply(lambda x: x.month_name())
    # Get Data Where Only Spam Messages
    spam_messages = getSpamData(data)
    # Get Frequency of spam messages according to months
    print(getBarChartPlot(spam_messages))
    st.bar_chart(spam_messages)


if __name__ == '__main__':
    main()