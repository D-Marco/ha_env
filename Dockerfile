from python:3.7-alpine
ARG docEnv
ENV docEnv $docEnv
workdir /usr/local/src
copy src/ /usr/local/src
run pip3 install -r requirements.txt
cmd python3 main.py 

