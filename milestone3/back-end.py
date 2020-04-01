#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 20:00:58 2020

@author: fengyuzou
"""

from __future__ import unicode_literals

import os
import sys
import redis
import requests
from bs4 import BeautifulSoup
import re
from random import randint, sample
import random
import json
import time,datetime

from argparse import ArgumentParser

from flask import Flask, request, abort, json
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cor = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# obtain the port that heroku assigned to this app.
heroku_port = os.getenv('PORT', None)

myDict = {}

@app.route("/callback", methods=['GET'])
@cross_origin(origin='*', allow_headers=['Content-Type'])
def callback():
    header = request.headers

    res = requests.get('https://www.hjenglish.com/new/p1297642/')

    bs = BeautifulSoup(res.text, 'lxml')
    alltitles = []
    v1 = bs.find('div', {'class':'article-content'})
    v = v1.find('p')

    words = re.findall(r'([1-9][1-9]*.)(.*?)(<br/>)',str(v))
    container = {}
    for line in words:
        if line[0] != '180':
            cn = re.findall(r'[\u4e00-\u9fa5]*.*?[\u4e00-\u9fa5]',line[1].replace('.','').replace('\xa0',"").strip())
            en = re.findall(r'\s[a-zA-Z]*[0-9]*[a-zA-Z]*',line[1].replace('.','').replace('\xa0',"").strip())
            ennew = " ".join(en).strip()
            cnnew = "".join(cn).strip()
            container[ennew] = cnnew
         
    containernew = {}
    for i in range(5):
        testsample = sample(list(container.keys()),3)
        answer = sample(list(container.values()),3)
        answer.append(container[testsample[0]])
        random.shuffle(answer)
        answernew = "-".join(answer)
        keynew = "-".join([testsample[0],container[testsample[0]]])
        containernew[keynew] = answernew
    return containernew

@app.route("/news", methods=['GET'])
@cross_origin(origin='*', allow_headers=['Content-Type'])
def news():
    header = request.headers
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia?from=dxy&source=&link=&share='

    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    ccc = BeautifulSoup(res.text,'html.parser')
    ssbb = ccc.find_all('script', id="getTimelineService1")
    list_all = []
    container = []
    containerdict = {}
    time.sleep(3)
    matchSentences = re.findall(r"\{\"id\":.*?\}",str(ssbb))
    for matchElement in matchSentences:
        dict_match_ele = eval(matchElement)
        dict_match_ele.pop("id")
        now = int(dict_match_ele["pubDate"])
        timeArray = time.localtime(now/1000)
        dict_match_ele["pubDate"]= time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
        container.append(dict_match_ele)
    containerdict["news"] = container
    return containerdict

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request. %s', e)
    return "An internal error occurs", 500

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--debug] [--help]'
    )
    arg_parser.add_argument('-p', '--production', action='store_true', help='Indicate this is production, not debug')
    options = arg_parser.parse_args()

    if options.production:
        app.run(host='0.0.0.0', debug=False, port=heroku_port)
    else:
        app.run(host='127.0.0.1', debug=True)