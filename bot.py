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

#respond to test thread with "Hello World"
def comment():
    for submission in subreddit.hot(limit = 10):
        if (submission.title == "Black Positivity Bot Test Thread"):
            submission.reply("Hello World!")
            print("Bot commenting Hello World!")

#search for keyphrase and respond with "Hello!"
def callbot():
    for comment in subreddit.stream.comments():
        try:
            if keyphrase in comment.body and not comment.saved :
                comment.reply("Hello!")
                comment.save()
                print("Bot responding to keyphrase with Hello!")
        except praw.exceptions.APIException:
            pass


callbot()
