# def print_hi(name):
#     print(f'Hi, {name}')
#
# if __name__ == '__main__':
#     print_hi('PyCharm')

import streamlit as st
import preprocess
import helper

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from helper import most_common_words

st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocess.preprocess(data)
    st.dataframe(df)

    user_list = df["user"].unique().tolist()
    user_list.remove("group notfication")
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user  = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        col1,col2 = st.columns(2)
        num_messages,words,media_messages,total_links= helper.f(selected_user,df)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        col3,col4 = st.columns(2)
        with col3:
            st.header("Media Shared")
            st.title(media_messages)
        with col4:
            st.header("Total Links")
            st.title(total_links)

        if selected_user == "Overall":
            st.title("Most busy Users ")
            name,count,new_df  = helper.fetch_most_busy_users(df)
            fig ,ax = plt.subplots()

            col1,col2 = st.columns(2)
            with col1:
                ax.bar(name,count,color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        df_wc = helper.generate_wc(selected_user, df)
        st.title("Word Cloud")
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        most_common_words_df = most_common_words(selected_user,df)
        # st.dataframe(most_common_words_df)

        def  add_labels(X,y):
            for i in range(X.shape[0]):
                plt.text(y[i],i,y[i],va="center",color="blue")

        st.title("Most Common Words")
        fig,ax = plt.subplots()
        ax.barh(most_common_words_df[0],most_common_words_df[1],color="blue")
        plt.xticks(rotation="vertical")
        add_labels(most_common_words_df[0],most_common_words_df[1])
        ax.set_xticks([])
        plt.show()
        st.pyplot(fig)

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            # fig, ax = plt.subplots()
            # ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            # st.pyplot(fig)
            pass

