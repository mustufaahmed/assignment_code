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
    # print(getBarChartPlot(spam_messages))
    data = [[30, 25, 50, 20],
    [40, 23, 51, 17],
    [35, 22, 45, 19]]
    X = np.arange(4)
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(X + 0.00, data[0], color = 'b', width = 0.25)
    ax.bar(X + 0.25, data[1], color = 'g', width = 0.25)
    ax.bar(X + 0.50, data[2], color = 'r', width = 0.25)

if __name__ == '__main__':
    main()