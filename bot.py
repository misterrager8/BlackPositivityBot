import praw

reddit = praw.Reddit(client_id= '',
                     client_secret= '',
                     username = '',
                     password = '',
                     user_agent = 'Black Positivity Bot')

#subreddit where bot lives
subreddit = reddit.subreddit('ObsidianTech')

#keyphrase to activate bot
keyphrase = '!bpb'

#respond to specified thread with comment
def comment():
    submission_title = 'Black Positivity Bot Test Thread'
    comment_text = 'Hello World!'
    for submission in subreddit.hot(limit = 10):
        if (submission.title == submission_title):
            submission.reply(comment_text)
            print('Bot commenting', comment_text)

#search for keyphrase and respond to comment
def callbot():
    comment_text = 'Hello!'
    for comment in subreddit.stream.comments():
        try:
            if keyphrase in comment.body and not comment.saved :
                comment.reply(comment_text)
                comment.save()
                print('Bot responding to keyphrase with', comment_text)
        except praw.exceptions.APIException:
            pass

#create a thread in subreddit
def post_thread():
    title = 'Bot Posted Test Thread'
    post_content = 'Black Positivity Bot test'
    subreddit.submit(title, selftext=post_content)
    print('"'+ title + '" submission created')

post_thread()
