# How to build a social media sentiment analysis pipeline with scikit-learn
A series of Jupyter notebooks that illustrate how to build a robust sentiment pipeline in scikit-learn. You can see the posts on my blog at https://ryan-cranfill.github.io/sentiment-pipeline-sklearn-1. Our use case here is sentiment classification of Twitter posts.
# Requirements
pandas
NumPy
scikit-learn (>= 0.18)
Twython (for getting Twitter data)
NTLK
pandas_confusion (for neato confusion matrices)
Jupyter (if you want to run the notebooks yourself)
# Setup
If you want to fetch the Twitter data locally, you'll need to populate the variables for Twitter API app key and secret, plus a user token and secret at the top the file `fetch_twitter_data.py`. You can create a Twitter API app [here](https://apps.twitter.com/app/new).