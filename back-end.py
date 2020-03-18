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

from argparse import ArgumentParser

from flask import Flask, request, abort, json
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cor = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# obtain the port that heroku assigned to this app.
heroku_port = os.getenv('PORT', None)

myDict = {}

@app.route("/callback", methods=['POST'])
@cross_origin(origin='*', allow_headers=['Content-Type'])
def callback():
    header = request.headers
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    #url = requests.get('https://www.shanbay.com/api/v1/vocabtest/category/')
    #js_link = url.json()
    #ciku = js_link['data'][1][0]
    test1_GMAT = {'a':'service','b':'flask','c':'load','d':'category','e':'information'}
    test2_GRE = {'a':'restart','b':'with','c':'stat','d':'type','e':'line'}
    test3_Tof = {'a':'instead','b':'use','c':'it','d':'value','e':'march'}
    ciku = [test1_GMAT,test2_GRE,test3_Tof]
    #words = test.json()
#    danci = []
#    words_knows = []
#    not_knows = []
#    print ('它来啦它来啦它带着测试过来啦，如果你认识这个单词，请输入1，不认识就敲2噢，好现在开始！')
    
    #if body in myDict:
     #  myDict[body] += 1
    #else:
     #   myDict[body] = 1

    #replydata = {'input' : body}
    #replydata['count'] = myDict[body]
    return ciku[int(body)]


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