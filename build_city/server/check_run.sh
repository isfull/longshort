#! /bin/bash
pid=`ps aux| grep  CityMain | grep -v 'grep'| awk -F ' ' '{print $2}' `
echo "pid:${pid}" >> check.log
echo `date` >> check.log
echo "pid:${pid}"
echo `date` 
bt_num=`tail -n 100 city.log | grep "Traceback (most recent call last)"|wc -l `
if [ $bt_num -gt 0 ];then
    echo "program done, restart" >> check.log
    echo "program done, restart"
    kill -9 $pid
    sleep 3
    mv city.log city_`date "+%Y_%m_%d_%H_%M_%S"`.log
    nohup python CityMain.py &
fi
