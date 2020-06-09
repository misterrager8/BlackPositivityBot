FROM python:2.717-slim
ADD bot.py /
ADD requirements.txt /
RUN pip install -r requirements.txt

ARG env="prod"
ENV env = ${env}
ARG username="default"
ENV username=${username}
ARG password="default"
ENV password = ${password}
ARG userAgent="Black Positivity Bot"
ENV userAgent=${userAgent}
ARG clientId="default"
ENV clientId=${clientId}
ARG clientSecret="default"
ENV clientSecret=${clientSecret}

ENTRYPOINT praw_username=${username} praw_user_agent=${userAgent} praw_password=${password} praw_client_secret=${clientSecret} praw_client_id=${clientId}} env=${env} python bot.py