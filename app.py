import streamlit as st
import matplotlib.pyplot as plt
import preprocessor
from wordcloud import WordCloud
import helper
# st.set_page_config(layout="wide", page_title="My Streamlit App", page_icon="🎈", theme="dark")

st.sidebar.title("this is my app")

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocess(data)

    # st.dataframe(df)
    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    st.title("Top Statistics")
    if st.sidebar.button("show analysis"):
        col1, col2, col3, col4 = st.columns(4)
        num_messages,words,media,links = helper.fetch_stats(selected_user,df)
        # Add content to each column
        with col1:
            st.header("Total messages")
            st.title(num_messages)
            # Add your content for column 1 here

        with col2:
            st.header("Total Words")
            st.title(words)
            # Add your content for column 2 here

        with col3:
            st.header("Total Media Shared")
            st.title(media)

        with col4:
            st.header("Total Links Shared")
            st.title(links)
            # Add your content for column 4 here
        x,cr_df = helper.fetch_mostbusyusers(df)
        st.title("mostbusyusers")
        st.header(x)
        st.dataframe(cr_df)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x = helper.fetch_mostbusyusers(df)
            fig, ax = plt.subplots()
            col1, col2, = st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
        st.title("Most Frequently used Words")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most comman words
        most_comman_w = helper.most_comman_words(selected_user,df)
        st.dataframe(most_comman_w)
        fig,ax= plt.subplots()
        ax.barh(most_comman_w[0], most_comman_w[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.header("Timeline")
        # timeline code
        timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
        time = []
        for i in range(timeline.shape[0]):
            time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
        timeline['time'] = time
        fig,ax= plt.subplots()
        plt.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        plt.title('Message Timeline')

        st.header("Monthly_timeline")

        df['only_date'] = df['date'].dt.date
        daily_timeline = df.groupby('only_date').count()['message'].reset_index()
        plt.figure(figsize=(15, 10))
        fig, ax = plt.subplots()
        plt.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)