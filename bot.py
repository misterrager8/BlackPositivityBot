# coding=utf-8
import datetime
import json

import arrow
import praw
import requests

reddit = praw.Reddit()

# subreddit where bot lives
subreddit = reddit.subreddit(reddit.config.custom['subreddit'])

# env check
print("Where am I? " + subreddit.display_name)


# http call to API, return random quote and its contributor
def quote():
    url = "http://blackpositivityquotes.tk/api/Quotes/fresh"
    req = requests.get(url)
    data = json.loads(req.text)
    quote_text = data["quote"].strip()
    if quote_text.startswith('“'):
        quote_text = quote_text[1:-1]
    contributor = data["contributor"]

    return '"{}", {}'.format(quote_text, contributor)


# respond to specified thread with comment
def comment():
    submission_title = 'Black Positivity Bot Test Thread'
    comment_text = 'Hello World!'
    for submission in subreddit.hot(limit=10):
        if submission.title == submission_title:
            submission.reply(comment_text)
            print('Bot commenting', comment_text)


# create a thread in subreddit
def post_thread():
    right_now = datetime.datetime.now()
    title = "Black Positivity Quote - " + right_now.strftime("%m/%d/%Y")
    post_content = quote() + "\n\nHappy " + right_now.strftime("%A") + ", fellas!"
    subreddit.submit(title, selftext=post_content)
    print('"{}" submission created'.format(title))


# returns list of subs user has commented in
def get_user_subs(username):
    user = reddit.redditor(username)
    unique_subs = []

    for comms in user.comments.new():
        if comms.subreddit.display_name not in unique_subs:
            unique_subs.append(comms.subreddit.display_name)

    return unique_subs


# returns date the account was created
def get_account_age(username):
    user = reddit.redditor(username)
    utc = arrow.Arrow.fromtimestamp(user.created_utc)
    date_formatted = utc.to('America/New_York').format("MMM D, YYYY")

    return date_formatted


# returns the user's karma score
def get_account_karma(username):
    user = reddit.redditor(username)
    return user.comment_karma


# keyphrases and bot responses
keyphrases = {'!bpb': 'Need some advice?', '!inspire': quote, '!uplift': quote, '!motivate': quote,
              'love y\'all': quote}


# search for keyphrase and respond to comment
def call_bot():
    for new_comment in subreddit.stream.comments():
        for phrase in keyphrases:
            try:
                if phrase in new_comment.body and not new_comment.saved:
                    if callable(keyphrases[phrase]):
                        comment_text = keyphrases[phrase]()
                        new_comment.reply(comment_text)
                    else:
                        comment_text = keyphrases[phrase]
                        new_comment.reply(comment_text)
                    new_comment.save()
                    print('Bot responding to', phrase, 'with:', comment_text)
            except praw.exceptions.APIException as error:
                print(error)
                pass


if __name__ == "__main__":
    call_bot()
    # print(get_account_karma(""))
    # print(get_account_age(""))
    # print(get_user_subs(""))
    # post_thread()
