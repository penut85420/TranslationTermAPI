FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN apt-get update && apt-get install -y ca-certificates
RUN pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
COPY ./ /app