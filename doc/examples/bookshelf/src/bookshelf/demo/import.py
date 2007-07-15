#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xmlrpclib import ServerProxy
from sys import argv, maxint

if __name__=='__main__':
    from collection import collection
    collection = [{'title':book['title'].replace('/', '')} for book in collection]
    instance = argv[1]
    if len(argv)==3:
        qty = int(argv[2])
    else:
        qty = maxint
    srv = ServerProxy("http://localhost:8080/%s/shelf" % instance)
    for book in collection:
        try:
            #print srv.add({'title':book['title'].encode('ascii', 'replace').replace('/', '')})
            srv.addbook(book)
        except TypeError:
            pass
        qty -= 1
        if qty == 0: break
