#!/usr/bin/env python
# coding: utf-8

# yum install epel-release -y
# yum install python-pip sysstat -y
# pip install -i https://mirrors.aliyun.com/pypi/simple elasticsearch

# Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
# sda               0.01     0.26    4.97    2.74     0.26     0.22   129.25     0.01    0.85    0.63    1.24   0.30   0.23
# sdb               0.01     0.26    4.97    2.74     0.26     0.22   129.25     0.01    0.85    0.63    1.24   0.30   0.23


import commands
import socket
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts="192.168.200.100:9200")
today = (datetime.utcnow().isoformat())[:10]
index = "iostat_disk_" + today
hostname = socket.gethostname()
newList = []

_, result = commands.getstatusoutput("iostat -d -x -m 2 21 | sed -n '/^Linux*\|^Device*\|^$/!p' | sed -n '2,$p'")

for i in result.split('\n'):
    newList.append((' '.join(i.split())).split())


if (es.indices.exists(index=index)) is False :
    es.indices.create(index=index,
                      body={"mappings":{"_doc":{"properties": {
                            "Device": {"type": "text"},
                            "rrqm/s": {"type": "float"},
                            "wrqm/s": {"type": "float"},
                            "r/s": {"type": "float"},
                            "w/s": {"type": "float"},
                            "rMB/s": {"type": "float"},
                            "wMB/s": {"type": "float"},
                            "avgrq-sz": {"type": "float"},
                            "vgqu-sz": {"type": "float"},
                            "await": {"type": "float"},
                            "r_await": {"type": "float"},
                            "w_await": {"type": "float"},
                            "svctm": {"type": "float"},
                            "%util": {"type": "float"},
                            "hostname": {"type": "text"},
                            "timestamp": {"type": "date"}
                      }}}})
else:
    pass


for temp in newList:
    doc = {
            'Device': temp[0],
            'rrqm/s': temp[1],
            'wrqm/s': temp[2],
            'r/s': temp[3],
            'w/s': temp[4],
            'rMB/s': temp[5],
            'wMB/s': temp[6],
            'avgrq-sz': temp[7],
            'vgqu-sz': temp[8],
            'await': temp[9],
            'r_await': temp[10],
            'w_await': temp[11],
            'svctm': temp[12],
            '%util': temp[13],
            'hostname': hostname,
            'timestamp': datetime.utcnow().isoformat(),
        }
    res = es.index(index=index, doc_type="_doc", body=doc)

