#!/usr/bin/python
#-*- coding: UTF8 -*-

import pandas as pd
import geocoder
import time

part = 0


df = pd.read_csv('hospbsc.csv',encoding='UTF8')
df.columns=['area','id','name','address','phone-code', 'phone', 'level', 'code','type','close_date' ]
df = df[df.level.isin([u'1',u'2',u'3',u'4'])] #只算醫療院所

addr= df.address.tolist()
hid = df.id.tolist()
addr_list = zip(hid, addr)

print 'size of df : ',len(addr_list)

def div(l, n):
    N = len(l)
    g = int(N/n)
    r = []
    for i in range(g+1):
        r.append(l[i*n:n*(i+1)+1])
    return r

result =[]
to_solve = div(addr_list, 2400)[part]
#to_solve = div(addr_list, 25)[part]


for i, entity in enumerate(to_solve):
    hid,addr = entity
    g = geocoder.api.Google(addr)
    d = dict()
    d['hid'] = hid
    d['confidence'] = g.confidence
    d['lat'] = g.lat
    d['lng'] = g.lng
    d['address'] = addr
    d['status'] = g.status
    #print repr(d)
    print '{}/2400, part={}'.format(i,part), g.status
    result.append(d)

r = pd.DataFrame(result)
r.to_csv('./result_{}.csv'.format(part), encoding='utf-8')


