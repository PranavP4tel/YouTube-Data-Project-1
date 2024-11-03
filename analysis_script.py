import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
from googleapiclient.discovery import build
from config import API_KEY
from collections import Counter
import itertools


import warnings
warnings.filterwarnings('ignore')

import isodate

def get_category(api_key):
    youtube = build('youtube','v3', developerKey = api_key)
    request = youtube.videoCategories().list(
        part = 'snippet',
        regionCode='IN'
    )

    response = request.execute()
    category_mapping = {}
    for item in response['items']:
        category_id = int(item['id'])
        category_name = item['snippet']['title']
        category_mapping[category_id] = category_name
    
    return category_mapping

#Obtaining video categories
category_map = get_category(API_KEY)

#Reading the data from csv file
videos = pd.read_csv('Trending_Videos.csv')
print(videos.head(), end = '\n\n')

#Adding category names to the dataframe
videos['category_name'] = videos['category_id'].map(category_map)

#Saving the file to csv
videos.to_csv('Trending_Videos.csv', index=False)

#Reading the saved file
videos = pd.read_csv('Trending_Videos.csv')
print(videos.isna().sum(), end = '\n\n')
print(videos.info(), end = '\n\n')
print(videos.describe(), end = '\n\n')

#Filling missing description values
videos.description.fillna('Not Available', inplace = True)
videos.published_at = pd.to_datetime(videos.published_at)
videos.tags = videos.tags.apply(lambda x: eval(x) if isinstance(x, str) else x)

#Visualizing distribution of views, likes and comments
fig,axes = plt.subplots(1,3,figsize= (18,7))

sns.histplot(data = videos, x = 'view_count', bins = 25, kde=True, ax = axes[0], color = 'red')
axes[0].set_title("Distribution of Views")
axes[0].set_xlabel("View count")
axes[0].set_ylabel("Frequency")

sns.histplot(data = videos, x = 'like_count', bins = 25, kde=True, ax = axes[1], color = 'green')
axes[1].set_title("Distribution of Likes")
axes[1].set_xlabel("Likes Count")
axes[1].set_ylabel("Frequency")

sns.histplot(data = videos, x = 'comment_count', bins = 25, kde=True, ax = axes[2], color = 'blue')
axes[2].set_title("Distribution of Comments")
axes[2].set_xlabel("Comment Count")
axes[2].set_ylabel("Frequency")

plt.tight_layout()
plt.show()

#Barplot for distribution per category
plt.figure(figsize = (18,7))
sns.countplot(y=videos['category_name'], order = videos['category_name'].value_counts().index,palette='plasma')
plt.title("Number of videos per category")
plt.xlabel("Number of Videos")
plt.ylabel("Category")
plt.show()

#Average engagement metric by category
category_metric = videos.groupby('category_name')[['view_count','like_count','dislike_count', 'comment_count']].mean().sort_values(by='view_count', ascending=False)

#Views by category
fig, axes = plt.subplots(1,3, figsize = (10,6))
sns.barplot(x=category_metric.view_count, y=category_metric.index, palette='crest', ax=axes[0])
axes[0].set_xlabel('View Count')
axes[0].set_ylabel('Category')
axes[0].set_title('Average Views Per Category')

#Likes by category
sns.barplot(x=category_metric.like_count, y=category_metric.index, palette='crest', ax=axes[1])
axes[1].set_xlabel('Likes Count')
axes[1].set_ylabel('')
axes[1].set_title('Average Likes Per Category')

#Comments by category
sns.barplot(x=category_metric.comment_count, y=category_metric.index, palette='crest', ax=axes[2])
axes[2].set_xlabel('Comment Count')
axes[2].set_ylabel('')
axes[2].set_title('Average Comments Per Category')

plt.tight_layout()
plt.show()

#Converting the duration form ISO format to seconds, and then grouping duration into seperate classes/bins
videos['duration'] = videos['duration'].apply(lambda x:isodate.parse_duration(x).total_seconds())
videos['duration_mins']=pd.cut(videos['duration'], bins=[0,300,600,1200,3600,7200], labels = ['0-5 mins','5-10 mins','10-120 mins','20-60 mins','60-120 mins'])

#Average engagement metric by video duration
duration_metric = videos.groupby('duration_mins')[['view_count','like_count', 'comment_count']].mean().sort_values(by='view_count', ascending=False)

#Views by duration
fig, axes = plt.subplots(1,3, figsize = (18,7))
sns.barplot(x=duration_metric.view_count, y=duration_metric.index, palette='mako', ax=axes[0])
axes[0].set_xlabel('View Count')
axes[0].set_ylabel('Duration')
axes[0].set_title('Average Views By Duration')

#Likes by duration
sns.barplot(x=duration_metric.like_count, y=duration_metric.index, palette='mako', ax=axes[1])
axes[1].set_xlabel('Likes Count')
axes[1].set_ylabel('')
axes[1].set_title('Average Likes By Duration')

#Comments by duration
sns.barplot(x=duration_metric.comment_count, y=duration_metric.index, palette='mako', ax=axes[2])
axes[2].set_xlabel('Comment Count')
axes[2].set_ylabel('')
axes[2].set_title('Average Comments By Duration')

plt.tight_layout()
plt.show()

#Tags by views
videos['tags_count'] = videos['tags'].apply(len)
plt.figure(figsize = (10,6))
sns.scatterplot(x='tags_count',y='view_count', data=videos, palette='rocket', alpha=0.7)
plt.xlabel('Number of Tags')
plt.ylabel('Number of Views')
plt.title('Views against the number of tags')
plt.show()

#Understanding influence of video publishing hour on the number of views
videos['publish_hour'] = videos['published_at'].dt.hour

plt.figure(figsize= (10,7))
sns.countplot(x=videos.publish_hour, palette='mako')
plt.xlabel('Hour of Publishing')
plt.ylabel('Number of videos')
plt.title('Distribution of videos by hour of publishing')
plt.show()

#Heatmap for correlation
plt.figure(figsize = (10,6))
sns.heatmap(videos[['category_id','view_count','like_count','comment_count','duration']].corr(), annot=True,  cmap = 'rocket')
plt.title("Correlation among attributes")
plt.show()


#Evaluating recurrence of words in the tags
#Flattening the tags column
all_words = list(itertools.chain.from_iterable(videos['tags']))

#Counting recurrence of words
word_count = Counter(all_words)
top_10 = word_count.most_common(10)
print(top_10)
words, counts = zip(*top_10)

#Plotting top 10 words
plt.figure(figsize=(10,6))
sns.barplot(x=words, y=counts, color='coral')
plt.title('Top 10 Tags')
plt.xlabel('Tags')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()