from re import I
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from wordcloud import WordCloud
from collections import Counter

# Downloads
st.set_page_config(layout="wide")
nltk.download('punkt')

# return spam data and input dataframe
def getSpamData(data):
    return data[data['Label'] == 'Spam']

# return non-spam data and input dataframe
def getNotSpamData(data):
    return data[data['Label'] == 'Non-Spam']

# get the data and return in tokenize form
def tokenizeTextIntoWords(column):
    result = ""
    for text in column:
        if text:
            result += " ".join(word_tokenize(text))+" "
    return result

# visualize bar chart data
def getBarChartPlot(data,color="blue"):
    monthly_count = data.groupby('Month')['Message_body'].count().sort_values(ascending=True)
    fig = plt.figure(figsize=(11,5), dpi=100)
    plt.bar(monthly_count.index, height=monthly_count.values,color=color)
    st.pyplot(fig)

# Generate WordCloud
def generateWordCloud(data):
    wordcloud = WordCloud(width = 800, height = 300,
                background_color ='black',
                min_font_size = 10).generate(data)
    # plot the WordCloud image                      
    fig = plt.figure(figsize = (8, 8), facecolor = None, dpi=100)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.show()
    st.pyplot(fig)
    return

# group data according to date 
def getMessagesGroupByDate(df,message_type):
    if message_type == 'spam':
        result = getSpamData(df).groupby('Date_Received')['Message_body'].count()
    else:
        result = getNotSpamData(df).groupby('Date_Received')['Message_body'].count()
    return result

# Visualize 10 common words in data
def getTenCommonWords(df,message_type,color="blue"):
    if message_type == 'spam':
        result = getSpamData(df)
    else:
        result = getNotSpamData(df)

    cnt = Counter()
    for text in result["Message_body"].values:
        for word in text.split():
            cnt[word] += 1
    common_words = cnt.most_common(10)
    words = []
    freq = []
    for item in common_words:
        words.append(item[0])
        freq.append(item[1])
    fig = plt.figure(figsize=(11,5), dpi=100)
    plt.barh(words, freq,color=color)
    plt.show()
    st.pyplot(fig)
    return



# get line Chart
def plot_df(df, x, y, title="", color="blue", xlabel='Date', ylabel='Number of Messages', dpi=100):
    fig = plt.figure(figsize=(15,4), dpi=dpi)
    plt.plot(x, y, color=color)
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()
    st.pyplot(fig)
    return

def main():
    # Main Heading
    st.title("SMS Data Analysis")
    # add file uploader
    uploaded_file = st.file_uploader("Choose a file")
    # read static file hardcode given
    data = pd.read_csv("SMS_data.csv",encoding='unicode_escape')
    # convert date column type to datetime which is object
    data['Date_Received'] = pd.to_datetime(data['Date_Received'])
    # create a new column of month
    data['Month'] = data['Date_Received'].apply(lambda x: x.month_name())
    
    col1,col2 = st.columns(2)
    with col1:
        # Get Data Where Only Spam Messages
        spam_messages = getSpamData(data)
        # Get Frequency of spam messages according to months
        st.header("Frequency Of Spam Messages")
        getBarChartPlot(spam_messages)
    with col2:
        # Get Data Where Only Non Spam Messages
        non_spam_messages = getNotSpamData(data)
        # Get Frequency of non spam messages according to months
        st.header("Frequency Of Non Spam Messages")
        getBarChartPlot(non_spam_messages,"red")
    # generate word cloud to show frequent words in noth spam and non spam
    st.header("Wordcloud of Most Frequent Words")
    data_for_Word_cloud = tokenizeTextIntoWords(data.Message_body)
    generateWordCloud(data_for_Word_cloud)

    # Get Data Where Only Spam Messages
    spam_count = getMessagesGroupByDate(data,'spam')
    # Get spam messages trends
    st.header("Spam Messages Trends On Daily Basis")
    plot_df(data, x=spam_count.index, y=spam_count.values, title='Trend and Seasonality of Spam Messages on Daily Basis')

    # Get Data Where Only Spam Messages
    non_spam_count = getMessagesGroupByDate(data,'non-spam')
    # Get spam messages trends
    st.header("Non-Spam Messages Trends On Daily Basis")
    plot_df(data, x=non_spam_count.index, y=non_spam_count.values, title='Trend and Seasonality of Non-Spam Messages on Daily Basis',color='red')

    col3,col4 = st.columns(2)
    with col3:
        st.header("Top 10 Common Words In Spam")
        getTenCommonWords(data,'spam')
    with col4:
        st.header("Top 10 Common Words In Non-Spam")
        getTenCommonWords(data,'non-spam',color="red")

if __name__ == '__main__':
    main()