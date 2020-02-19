import praw
import json
import requests

reddit = praw.Reddit(client_id= '',
                     client_secret= '',
                     username = '',
                     password = '',
                     user_agent = 'Black Positivity Bot')

#subreddit where bot lives
subreddit = reddit.subreddit('ObsidianTech')

#http call to API, return random quote and its contributor
def quote():
    url = "http://blackpositivityquotes.tk/api/Quotes/random"
    req = requests.get(url)
    data = json.loads(req.text)
    quote_text = data["quote"].strip()
    if quote_text.startswith('“'):
        quote_text = quote_text[1:-1]
    contributor = data["contributor"]

    return '"{}", {}'.format(quote_text, contributor)

#respond to specified thread with comment
def comment():
    submission_title = 'Black Positivity Bot Test Thread'
    comment_text = 'Hello World!'
    for submission in subreddit.hot(limit = 10):
        if (submission.title == submission_title):
            submission.reply(comment_text)
            print('Bot commenting', comment_text)

#create a thread in subreddit
def post_thread():
    title = 'Bot Posted Test Thread'
    post_content = 'Black Positivity Bot test'
    subreddit.submit(title, selftext=post_content)
    print('"{}" submission created'.format(title))

#keyphrases and bot responses
keyphrases = {'!bpb':'Hello!', '!inspire':quote}

#search for keyphrase and respond to comment
def call_bot():
    for comment in subreddit.stream.comments():
        for phrase in keyphrases:
            try:
                if phrase in comment.body and not comment.saved :
                    if callable(keyphrases[phrase]):
                        comment_text = keyphrases[phrase]()
                        comment.reply(comment_text)
                    else:
                        comment_text = keyphrases[phrase]
                        comment.reply(comment_text)
                    comment.save()
                    print('Bot responding to', phrase, 'with:', comment_text)
            except praw.exceptions.APIException as error:
                print(error)
                pass

call_bot()
