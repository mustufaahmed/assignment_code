import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from wordcloud import WordCloud
import string
import seaborn as sns

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

    monthly_count = data.groupby('Month')['Message_body'].count().sort_values(ascending=True)
    sns.boxplot(x='Date_Received',y='Count',data=monthly_count.values,palette='rainbow')

if __name__ == '__main__':
    main()