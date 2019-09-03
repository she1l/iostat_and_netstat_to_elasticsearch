#!/usr/bin/env python
# coding: utf-8

# yum install epel-release -y
# yum install python-pip sysstat -y
# pip install -i https://mirrors.aliyun.com/pypi/simple elasticsearch

# ESTABLISHED 状态连接数：
# netstat -aultnp | grep ESTABLISHED | wc -l

# SYN_REC 状态连接数：
# netstat -aultnp | grep SYN_REC | wc -l

# TIME_WAIT 状态连接数：
# netstat -aultnp | grep TIME_WAIT | wc -l

# 检查 ESTABLISHED 连接并且列出每个IP地址的连接数量；
# netstat -aultnp | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr



import commands
import socket
import time
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts="192.168.200.100:9200")
today = (datetime.utcnow().isoformat())[:10]
index = "netstat_" + today
hostname = socket.gethostname()
newList = []

for i in range(1, 21):
    time.sleep(2)
    _, SYN_REC = commands.getstatusoutput('netstat -aultnp | grep SYN_REC | wc -l')
    _, TIME_WAIT = commands.getstatusoutput('netstat -aultnp | grep TIME_WAIT | wc -l')
    _, ESTABLISHED = commands.getstatusoutput('netstat -aultnp | grep ESTABLISHED | wc -l')
    newList.append([SYN_REC, TIME_WAIT, ESTABLISHED])


if (es.indices.exists(index=index)) is False :
    es.indices.create(index=index,
                      body={"mappings":{"_doc":{"properties": {
                            "SYN_REC": {"type": "float"},
                            "TIME_WAIT": {"type": "float"},
                            "ESTABLISHED": {"type": "float"},
                            "hostname": {"type": "text"},
                            "timestamp": {"type": "date"}
                      }}}})
else:
    pass


for temp in newList:
    doc = {
            'SYN_REC': temp[0],
            'TIME_WAIT': temp[1],
            'ESTABLISHED': temp[2],
            'hostname': hostname,
            'timestamp': datetime.utcnow().isoformat(),
        }
    res = es.index(index=index, doc_type="_doc", body=doc)


