import csv
import re
import pandas as pd
# import nltk
# nltk.download('vader_lexicon')
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
import plotly.express as px
import plotly.graph_objects as go
from colorama import Fore, Style
from typing import Dict
import streamlit as st
import re
import emoji
import statistics

def extract_video_id(youtube_link):
    video_id_regex = r"^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(video_id_regex, youtube_link)
    if match:
        video_id = match.group(1)
        return video_id
    else:
        return None
    
def comments_list(csv_file):
    comments = []
    with open(csv_file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            comments.append(row['Comment'])
    return comments


# Define a function to preprocess comments
def preprocess_comments(comments):
    # Abbreviation expansion mapping
    abbreviation_map = {
        "i'm": "i am",
        "you're": "you are",
        "it's": "it is",
        "we're": "we are",
        "they're": "they are",
        "don't": "do not",
        "won't": "will not",
        "can't": "cannot",
        "i've": "i have",
        "you've": "you have",
        "we've": "we have",
        "they've": "they have",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "there's": "there is",
        "that's": "that is",
        "who's": "who is",
        "what's": "what is",
        "let's": "let us",
        "i'll": "i will",
        "you'll": "you will",
        "he'll": "he will",
        "she'll": "she will",
        "we'll": "we will",
        "they'll": "they will",
        "didn't": "did not",
        "doesn't": "does not",
        "hasn't": "has not",
        "haven't": "have not",
    }

    preprocessed_comments = []

    for comment in comments:
        # Step 1: Remove extra whitespaces
        comment = " ".join(comment.split())

        # Step 2: Expand abbreviations
        words = comment.split()
        expanded_words = [
            abbreviation_map[word.lower()] if word.lower() in abbreviation_map else word
            for word in words
        ]
        comment = " ".join(expanded_words)

        # Step 3: Replace emojis with their textual descriptions
        comment = emoji.demojize(comment)

        # Step 4: Remove punctuations but preserve textual emoji descriptions
        comment = re.sub(r"[^\w\s:]", "", comment)

        # Add the cleaned comment to the result list
        preprocessed_comments.append(comment)

    return preprocessed_comments



def word_count_per_comment(preprocessed_comments):
    word_count_list = []
    for comment in preprocessed_comments:
        cl = comment.split()
        word_count_list.append(len(cl))
    return word_count_list

def median_count(word_count_list):
    if word_count_list:
        median_cnt = statistics.median(word_count_list)
    else:
        median_cnt = 0
    return median_cnt







    

# def analyze_sentiment(csv_file):
#     # Initialize the sentiment analyzer
#     sid = SentimentIntensityAnalyzer()

#     # Read in the YouTube comments from the CSV file
#     comments = []
#     with open(csv_file, 'r', encoding='utf-8-sig') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             comments.append(row['Comment'])

#     # Count the number of neutral, positive, and negative comments
#     num_neutral = 0
#     num_positive = 0
#     num_negative = 0
#     for comment in comments:
#         sentiment_scores = sid.polarity_scores(comment)
#         if sentiment_scores['compound'] == 0.0:
#             num_neutral += 1
#         elif sentiment_scores['compound'] > 0.0:
#             num_positive += 1
#         else:
#             num_negative += 1

#     # Return the results as a dictionary
#     results = {'num_neutral': num_neutral, 'num_positive': num_positive, 'num_negative': num_negative}
#     return results

# def bar_chart(csv_file: str) -> None:
#     # Call analyze_sentiment function to get the results
#     results: Dict[str, int] = analyze_sentiment(csv_file)

#     # Get the counts for each sentiment category
#     num_neutral = results['num_neutral']
#     num_positive = results['num_positive']
#     num_negative = results['num_negative']

#     # Create a Pandas DataFrame with the results
#     df = pd.DataFrame({
#         'Sentiment': ['Positive', 'Negative', 'Neutral'],
#         'Number of Comments': [num_positive, num_negative, num_neutral]
#     })

#     # Create the bar chart using Plotly Express
#     fig = px.bar(df, x='Sentiment', y='Number of Comments', color='Sentiment', 
#                  color_discrete_sequence=['#87CEFA', '#FFA07A', '#D3D3D3'],
#                  title='Sentiment Analysis Results')
#     fig.update_layout(title_font=dict(size=20))


#     # Show the chart
#     st.plotly_chart(fig, use_container_width=True)    
    
# def plot_sentiment(csv_file: str) -> None:
#     # Call analyze_sentiment function to get the results
#     results: Dict[str, int] = analyze_sentiment(csv_file)

#     # Get the counts for each sentiment category
#     num_neutral = results['num_neutral']
#     num_positive = results['num_positive']
#     num_negative = results['num_negative']

#     # Plot the pie chart
#     labels = ['Neutral', 'Positive', 'Negative']
#     values = [num_neutral, num_positive, num_negative]
#     colors = ['yellow', 'green', 'red']
#     fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
#                                  marker=dict(colors=colors))])
#     fig.update_layout(title={'text': 'Sentiment Analysis Results', 'font': {'size': 20, 'family': 'Arial', 'color': 'grey'},
#                               'x': 0.5, 'y': 0.9},
#                       font=dict(size=14))
#     st.plotly_chart(fig)
    
    
    
# def create_scatterplot(csv_file: str, x_column: str, y_column: str) -> None:
#     # Load data from CSV
#     data = pd.read_csv(csv_file)

#     # Create scatter plot using Plotly
#     fig = px.scatter(data, x=x_column, y=y_column, color='Category')

#     # Customize layout
#     fig.update_layout(
#         title='Scatter Plot',
#         xaxis_title=x_column,
#         yaxis_title=y_column,
#         font=dict(size=18)
#     )

#     # Display plot in Streamlit
#     st.plotly_chart(fig, use_container_width=True)
    
    
    
# def print_sentiment(csv_file: str) -> None:
#     # Call analyze_sentiment function to get the results
#     results: Dict[str, int] = analyze_sentiment(csv_file)

#     # Get the counts for each sentiment category
#     num_neutral = results['num_neutral']
#     num_positive = results['num_positive']
#     num_negative = results['num_negative']

  
#     # Determine the overall sentiment
#     if num_positive > num_negative:
#         overall_sentiment = 'POSITIVE'
#         color = Fore.GREEN
#     elif num_negative > num_positive:
#         overall_sentiment = 'NEGATIVE'
#         color = Fore.RED
#     else:
#         overall_sentiment = 'NEUTRAL'
#         color = Fore.YELLOW

#     # Print the overall sentiment in color
#     print('\n'+ Style.BRIGHT+ color + overall_sentiment.upper().center(50, ' ') + Style.RESET_ALL)



