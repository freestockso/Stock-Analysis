#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,logging
if sys.version > (3,0):
    import urllib.request as request
else:
    import urllib as request

DEBUG=False

def get(url):
    response = request.urlopen(url)
    return response.read()

def fetch(url):
    logging.debug("Start fetch url %s" %(url))
    if DEBUG:
        data = get(url)   
        #logging.debug(data)
        return data
    else:
        try:
            return get(url)   
        except:
            logging.warning("Fetching url %s was fail, try once again." %url)
            try:
                return get(url)
            except:
                logging.error("Error happened when Fetching url %s.Give it up." %url)
