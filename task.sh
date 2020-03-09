#!/bin/bash
service_name='@run ur task@'
TaskFile='Task.py'


function start(){
   echo "开始启动任务..."
   
   python3 $TaskFile & echo 'explore proxyip task has start'
}

function stop(){
   echo "任务被中止..."
   
   python3 -c 'import Task;Task.close_task()' & echo 'explore proxyip task has stop'
}

case "$1" in
    "start")
      start $@
      echo "$!" > /tmp/ipproxy.pid
      exit 0
    ;;
    "stop")
      stop
      kill `cat /tmp/ipproxy.pid`
      exit 0
     ;;
    "restart")
       restart $@
       exit 0
     ;;
    *)
       echo "用法： $0 {start|stop|restart}"
       exit 1
    ;;
esac
exit 0
