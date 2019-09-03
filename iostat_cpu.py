#!/usr/bin/env python
# coding: utf-8

# yum install epel-release -y
# yum install python-pip sysstat -y
# pip install -i https://mirrors.aliyun.com/pypi/simple elasticsearch

# avg-cpu:  %user   %nice %system %iowait  %steal   %idle
#            0.00    0.00    7.00    0.50    0.00   92.50


import commands
import socket
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts="192.168.200.100:9200")
today = (datetime.utcnow().isoformat())[:10]
index = "iostat_cpu_" + today
hostname = socket.gethostname()
newList = []

_, result = commands.getstatusoutput("iostat -c 2 21 | sed -n '/^Linux*\|^avg-cpu*\|^$/!p' | sed -n '2,$p'")

for i in result.split('\n'):
    newList.append((' '.join(i.split())).split())


if (es.indices.exists(index=index)) is False :
    es.indices.create(index=index,
                      body={"mappings":{"_doc":{"properties": {
                            "%user": {"type": "float"},
                            "%nice": {"type": "float"},
                            "%system": {"type": "float"},
                            "%iowait": {"type": "float"},
                            "%steal": {"type": "float"},
                            "%idle": {"type": "float"},
                            "hostname": {"type": "text"},
                            "timestamp": {"type": "date"}
                      }}}})
else:
    pass


for temp in newList:
    doc = {
            '%user': temp[0],
            '%nice': temp[1],
            '%system': temp[2],
            '%iowait': temp[3],
            '%steal': temp[4],
            '%idle': temp[5],
            'hostname': hostname,
            'timestamp': datetime.utcnow().isoformat(),
        }
    res = es.index(index=index, doc_type="_doc", body=doc)

