_env=$1
_clientId=$2
_clientSecret=$3
_password=$4
_userAgent=$5
_username=$6

echo $_env
echo $_username
echo $_password
echo $_userAgent
echo $_clientId
echo $_clientSecret

pip3 install -r requirements.txt

praw_username=$_username praw_user_agent=$_userAgent praw_password=$_password praw_client_secret=$_clientSecret praw_client_id=$_clientId env=$_env python3 bot.py
