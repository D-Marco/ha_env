from python:3.7-alpine
ARG docEnv
#表示变量是docEnv，值是传递进来的docEnv的值
ENV docEnv $docEnv
workdir /usr/local/src
copy src/ /usr/local/src
run pip3 install -r requirements.txt
cmd python3 main.py 

