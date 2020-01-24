import praw

reddit = praw.Reddit(client_id= '',
                     client_secret= '',
                     username = '',
                     password = '',
                     user_agent = 'Black Positivity Bot')

#subreddit where bot lives
subreddit = reddit.subreddit('ObsidianTech')

#respond to test thread with "hello world"
def comment():

    for submission in subreddit.hot(limit = 10):
        if (submission.title == "Black Positivity Bot Test Thread"):
            print("Bot commenting hello world.")
            submission.reply("Hello Ashken!")

comment()
