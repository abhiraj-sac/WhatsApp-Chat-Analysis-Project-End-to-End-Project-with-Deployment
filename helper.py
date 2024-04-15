import pandas as pd
import streamlit
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

f = open('stop_hinglish.txt', 'r')
stop_words = f.read()
def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    num_message = df.shape[0]
    # number_of_words
    words = []
    for message in df['message']:
        words.extend(message.split())
    media = df[df['message'] == '<Media omitted>\n'].shape[0]

    extractor = URLExtract()
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    # len(links)

    return num_message, len(words), media, len(links)


def fetch_mostbusyusers(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'}
    )
    ans = pd.DataFrame(df)
    return x,df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp[temp['message'] != '<Media omitted>\n']
    f = open('stop_hinglish.txt', 'r')

    def remove_stop_word(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    # if selected_user != "Overall":
    # df = df[df['user'] == selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message']= temp['message'].apply(remove_stop_word)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_comman_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp[temp['message'] != '<Media omitted>\n']
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_comman_df = pd.DataFrame(Counter(words).most_common(20))
    return most_comman_df
def timeline(df):
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    plt.plot(timeline['time'], timeline['message'])
    plt.xticks(rotation="vertical")
    plt.xlabel('Time')
    plt.ylabel('Message')
    plt.title('Message Timeline')