docker rm -f m2m
docker rm -f mosquitto
kill -15 $(netstat -tunlp|grep 20905|grep -v grep|awk '{print $7}'|awk -F '/' '{print $1}')
kill -15 $(netstat -tunlp|grep 20805|grep -v grep|awk '{print $7}'|awk -F '/' '{print $1}')
sleep 3
netstat -tunlp|grep -E '20905|20805'|grep -v grep
if [ "$?" -eq 0 ]
then
  kill -2 $(netstat -tunlp|grep 20905|grep -v grep|awk '{print $7}'|awk -F '/' '{print $1}')
  kill -2 $(netstat -tunlp|grep 20805|grep -v grep|awk '{print $7}'|awk -F '/' '{print $1}')
fi
docker-compose up -d
