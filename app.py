import streamlit as st
import os
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from Senti import extract_video_id, comments_list, preprocess_comments, word_count_per_comment, median_count
from YoutubeCommentScrapper import save_video_comments_to_csv,get_channel_info,youtube,get_channel_id,get_video_stats
import re


stop_words = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves',
    'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
    'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
    'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up',
    'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
    'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
    'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
    'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn',
    'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn'
}




def delete_non_matching_csv_files(directory_path, video_id):
    for file_name in os.listdir(directory_path):
        if not file_name.endswith('.csv'):
            continue
        if file_name == f'{video_id}.csv':
            continue
        os.remove(os.path.join(directory_path, file_name))


st.set_page_config(page_title='yt analyse', page_icon = 'LOGO.png', initial_sidebar_state = 'auto')
#st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
st.sidebar.title("Yt Analysis")
st.sidebar.header("Enter YouTube Link")
youtube_link = st.sidebar.text_input("Link")
directory_path = os.getcwd()
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

def plot_word_count_distribution(word_count_list):
    # Create a DataFrame for grouping
    df = pd.DataFrame({'Word Count': word_count_list})
    
    # Group by word count and count occurrences
    distribution = df['Word Count'].value_counts().reset_index()
    distribution.columns = ['Word Count', 'Number of Comments']
    distribution = distribution.sort_values(by='Word Count')

    # Plot the data using Plotly
    fig = px.bar(
        distribution,
        x='Word Count',
        y='Number of Comments',
        title='Number of Comments vs. Word Count',
        labels={'Word Count': 'Number of Words', 'Number of Comments': 'Number of Comments'},
        color='Word Count',
        color_continuous_scale='Blues'
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

def generate_word_frequency_map(preprocessed_comments):
    # Combine all comments into one string
    all_words = " ".join(preprocessed_comments)
    
    # Split into individual words
    words = re.findall(r'\b\w+\b', all_words.lower())  # Match words, ignore case
    
    filtered_words = [word for word in words if word not in stop_words] 

    # Count the frequency of each word
    word_counts = Counter(filtered_words)
    
    return word_counts

def plot_word_cloud(word_counts):
    # Generate word cloud from the word counts
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
    
    # Display the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Turn off axis
    st.pyplot(plt)


if youtube_link:
    video_id = extract_video_id(youtube_link)
    channel_id = get_channel_id(video_id)
    if video_id:
        st.sidebar.write("The video ID is:", video_id)     
        csv_file = save_video_comments_to_csv(video_id)
        delete_non_matching_csv_files(directory_path,video_id)
        st.sidebar.write("Comments saved to CSV!")
        st.sidebar.download_button(label="Download Comments", data=open(csv_file, 'rb').read(), file_name=os.path.basename(csv_file), mime="text/csv")
        
        #using fn
        channel_info = get_channel_info(youtube,channel_id)
               
        col1, col2 = st.columns(2)

        with col1:
           channel_logo_url = channel_info['channel_logo_url']
           st.image(channel_logo_url, width=250)
           print("> logo")

        with col2:
           channel_title = channel_info['channel_title']
           st.title(' ')
           st.text("  YouTube Channel Name  ")
           #st.markdown('** YouTube Channel Name **')
           st.title(channel_title)
           st.title("  ")
           st.title(" ")
           st.title(" ")
           print("> channel name")
           
        
        #Using fn
        
        
        
        st.title(" ")
        col3, col4 ,col5 = st.columns(3)
        
        
        with col3:
           video_count=channel_info['video_count']
           st.header("  Total Videos  ")
           #st.subheader("Total Videos")
           st.subheader(video_count)
           print("> video count")

        with col4:
           channel_created_date= channel_info['channel_created_date']
           created_date = channel_created_date[:10]
           st.header("Channel Created ")
           st.subheader(created_date)
           print("> date created")

        with col5:
            
            st.header(" Subscriber_Count ")
            subs = int(channel_info["subscriber_count"])
            if subs < 1000:
                st.subheader(subs)
            elif subs >= 1000 and subs < 1000000:
                st.subheader(f"{subs/1000} K")
            elif subs >= 1000000:
                st.subheader(f"{subs/1000000} M")
            print(channel_info["subscriber_count"])
            print("> subscriber_count")
            
        st.title(" ")

        stats = get_video_stats(video_id)   
        
        st.title("Video Information :")
        col6, col7 ,col8 = st.columns(3)
        
        
        with col6:
            st.header("  Total Views  ")
           #st.subheader("Total Videos")
            st.subheader(stats["viewCount"])
            print("> total views")

        with col7:
           st.header(" Like Count ")
           st.subheader(stats["likeCount"])
           print("> like count")
           

        with col8:
            
            st.header(" Comment Count ")
            st.subheader(stats["commentCount"])
            print("> comment count")
            
        st.header(" ")  

        comments = comments_list(csv_file)
        preprocessed_comments = preprocess_comments(comments)
        word_count_list = word_count_per_comment(preprocessed_comments)
        median = median_count(word_count_list)

        col9, col10 = st.columns(2)

        with col9:
            st.header("Median Word Count")
            st.subheader(median)
            print(f"> median = {median}")

        with col10:

            st.header("Mean Word Count")
            num_comments = int(stats["commentCount"])
            mean = round(sum(word_count_list)/num_comments, 2)
            st.subheader(mean)
            print(f"> mean = {mean}")

        st.header(" ") 

        plot_list = []
        for it in word_count_list:
            if it < 125:
                plot_list.append(it)
            
                
        st.title("Word Count Distribution")
        plot_word_count_distribution(plot_list)

        st.header(" ") 

        st.title("Word Cloud Visualization")
        word_counts = generate_word_frequency_map(preprocessed_comments)
    
        # Plot word cloud
        plot_word_cloud(word_counts)

        st.header(" ") 
        
        
        _, container, _ = st.columns([10, 80, 10])
        container.video(data=youtube_link)

        
            
            
        
            
            
        # results = analyze_sentiment(csv_file)
        
        
        # col9, col10 ,col11 = st.columns(3)
        
        
        # with col9:
        #     st.header("  Positive Comments  ")
        #    #st.subheader("Total Videos")
        #     st.subheader(results['num_positive'])

        # with col10:
        #    st.header(" Negative Comments ")
        #    st.subheader( results['num_negative'])
           

        # with col11:
            
        #     st.header(" Neutral Comments ")
        #     st.subheader(results['num_neutral'])
        
        
        # bar_chart(csv_file)
        
        # plot_sentiment(csv_file)
        
            
        st.subheader("Channel Description ")   
        channel_description = channel_info['channel_description']
        st.write(channel_description)
        
    else:
        st.error("Invalid YouTube link")
        
        
  
    
    
        



