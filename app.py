from flask import Flask, abort, flash, redirect, render_template, request, url_for
from tweepy import TweepError, RateLimitError
from include import config
import tweepy, pprint, os, sys

app = Flask(__name__)
app.config['DEBUG'] = False
app.secret_key = config.img_key


@app.route('/', methods=['GET', 'POST'])
@app.route('index', methods=['GET', 'POST'])
def main():
    query = 'Twitter API test query'

    # Use environment variables in live version
    key = config.consumer_key
    secret = config.consumer_secret
    token = config.access_token
    token_secret = config.access_token_secret

    auth = tweepy.OAuthHandler(key, secret)
    auth.set_access_token(token, token_secret)

    api = tweepy.API(auth)
    pp = pprint.PrettyPrinter(indent=4)
    _tweets = []

    try:
        while len(_tweets) < 1:  # 10:
            for tweet in tweepy.Cursor(api.search, q=query, result_type='recent', include_rts=False, lang='en') \
                    .items(1):

                if 'RT' not in tweet.text \
                        and tweet.user.screen_name not in _tweets \
                        and tweet.text not in _tweets \
                        and len(_tweets) < 1 \
                        and tweet.user.profile_image_url:

                    appendtweet = {
                        'handle': tweet.user.screen_name,
                        'avi': str(tweet.user.profile_image_url_https),
                        'following': tweet.user.following,
                        'text': tweet.text,
                        'hashtags': []
                    }
                    if '_normal' in appendtweet['avi']:
                        _b = appendtweet['avi'].split('_normal')
                        appendtweet['avi'] = '%s_400x400%s' % (_b[0], _b[1])

                    if len(tweet.entities['hashtags']) > 0:
                        for h in tweet.entities['hashtags']:
                            appendtweet['hashtags'].append(h)

                    # print appendtweet['hashtags']
                    _tweets.append(appendtweet)

    except RateLimitError as r:
        return r.api_code

    return render_template('index.html', title='Home', posts=_tweets)


if __name__ == '__main__':
    app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 8080)))
