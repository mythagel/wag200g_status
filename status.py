from lxml import html
from itertools import izip
import requests
import os
import time
import datetime

def pairwise(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

def file_exists(filepath):
    try:
        f = open(filepath)
    except (IOError) as e:
        return False
    return True


user = "admin"
password = ""
server = "192.168.1.1"

while True :
    page = requests.get('http://' + user + ':' + password + '@' + server + '/setup.cgi?next_file=DSL_status.htm')
    tree = html.fromstring(page.text)
    status = tree.xpath('//table[@class="std"]/tr/td/text()')
    #print 'Status: ', status


    if not file_exists("status.csv") :
        f = open('status.csv', 'a')
        for header, value in pairwise(status):
            f.write('"' + header + '",');
        f.write('"timestamp"\n')

    f = open('status.csv', 'a')
    for header, value in pairwise(status):
        f.write('"' + value + '",');
    f.write('"' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '"')
    f.write('\n')
    time.sleep(5)


