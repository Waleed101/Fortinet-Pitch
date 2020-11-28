# quick notes: you need to have 'vader_lexicon' in the same folder as the script
# also need to pip install the follow
    # praw
    # textblob
    # nltk
 
# This code is also tailored to parse through subreddits on Reddit, but not entirely optimized for general
# webpages. To change that, you'd probably have to include beautiful soup and get all the general text.

import praw
from textblob import TextBlob
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
GENERAL_POLARITY = 0.0001

sia = SentimentIntensityAnalyzer() # creating the sentiment object

reddit = praw.Reddit(client_id='dwvhQN_PoUCoAw',
                     client_secret='X8N_SZUsiI-CNVIYLToBFFQ-cYE',
                     user_agent='news on hooks') 
                     # creating hook to the Reddit PRAW, this has been slowly phased out - so use with caution 

# grabbing all the posts, checkpoint is the subreddit, all is the time period (week, day etc.), limit maxes out at 1000
top_posts = reddit.subreddit('checkpoint').top('all', limit=1000)

# function to run the text blob sentiment, returns if Positive, Negative, Neutral
def text_blob_sentiment(review, sub_entries_textblob):
    analysis = TextBlob(review)
    if analysis.sentiment.polarity >= GENERAL_POLARITY: # grab the sentiment, if its greater than the general set polarity
        if analysis.sentiment.polarity > 0:
            sub_entries_textblob['positive']+=1 # add one to the positive array 
            return 'Positive'

    elif analysis.sentiment.polarity <= (-1*GENERAL_POLARITY):
        if analysis.sentiment.polarity <= 0:
            sub_entries_textblob['negative']+=1 # add one to the negative array
            return 'Negative'
    else:
        sub_entries_textblob['neutral']+=1 # add one to the neutral array
        return 'Neutral'
    
def nltk_sentiment(review, sub_entries_nltk): 
    # vader does it slightly differently, where it'll return the likeness of each one
    vs = sia.polarity_scores(review) # get polarity of the passed over string
    if not vs['neg'] > 0.05: # if the negative polarity is very low
        if vs['pos'] - vs['neg'] > 0: # and if the positive polarity is higher than negative polarity
            sub_entries_nltk['positive']+=1
            return 'Positive'
        else: # if its not, then assume is neutral
            sub_entries_nltk['neutral']+=1
            return 'Neutral'

    elif not vs['pos'] > 0.05: # if the positive polarity is very low
        if vs['pos'] - vs['neg'] <= 0: # and if the negative polarity is higher than positive polarity
            sub_entries_nltk['negative']+=1
            return 'Negative'
        else: # if its not, then assume is neutral
            sub_entries_nltk['neutral']+=1
            return 'Neutral'
    else: # if the negative and positive polarity are both not very high
        sub_entries_nltk['neutral']+=1 # then is neutral
        return 'Neutral'


def replies_of(top_level_comment, count_comment, sub_entries_textblob, sub_entries_nltk): # get replies, unneeded if you're not using reddit
    if len(top_level_comment.replies) == 0: # if there are no subcomments, exit the loop
        count_comment = 0
        return
    else:
        for num, comment in enumerate(top_level_comment.replies): # get all comments within the current post
            try: # this prevents an error
                count_comment += 1 # next comment
                text_blob_sentiment(comment.body, sub_entries_textblob) # textblob sentiment
                nltk_sentiment(comment.body, sub_entries_nltk) # vader sentiment
            except:
                continue
            replies_of(comment, count_comment, sub_entries_textblob,sub_entries_nltk) # get all the replies of the current comment


def main():
    textblob_all = [0, 0, 0]
    nltk_all = [0, 0, 0]
    post = 0
    for submission in top_posts: # cycle through all the posts
        sub_entries_textblob = {'negative': 0, 'positive' : 0, 'neutral' : 0}
        sub_entries_nltk = {'negative': 0, 'positive' : 0, 'neutral' : 0}
        text_blob_sentiment(submission.title, sub_entries_textblob)
        nltk_sentiment(submission.title, sub_entries_nltk)
        submission_comm = reddit.submission(id=submission.id)

        for count, top_level_comment in enumerate(submission_comm.comments):
            count_comm = 0
            try :
                text_blob_sentiment(top_level_comment.body, sub_entries_textblob)
                nltk_sentiment(top_level_comment.body, sub_entries_nltk)
                replies_of(top_level_comment,
                           count_comm,
                           sub_entries_textblob,
                           sub_entries_nltk)
            except:
                continue
        
        # track all the textblob sentiment
        textblob_all[0]+= sub_entries_textblob['negative']
        textblob_all[1]+= sub_entries_textblob['positive']
        textblob_all[2]+= sub_entries_textblob['neutral']
        
        # track all the vader sentiment
        nltk_all[0]+= sub_entries_nltk['negative']
        nltk_all[1]+= sub_entries_nltk['positive']
        nltk_all[2]+= sub_entries_nltk['neutral']
        print("On Post: " + str(post)) # keep track of the current post
        post+=1
    # print off all the sentiment    
    print('Over all Sentiment of Topic by TextBlob :', nltk_all)
    print('Over all Sentiment of Topic by VADER :', textblob_all)

# call the main function
main()