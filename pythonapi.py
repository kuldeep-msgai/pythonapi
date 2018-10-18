#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 00:22:23 2018

@author: kuldeep
"""

from flask import Flask, request
import mysql.connector
from flask import render_template
import json
import boto3
import urllib.request
import requests
from boto.s3.key import Key
from datetime import date, datetime, timedelta

s3 = boto3.resource('s3')


app = Flask(__name__)
@app.route("/")


def home(): 
     return render_template("home.html")
    


@app.route('/handle_data', methods=['POST'])
def handle_data():
    urlname = request.form['URL']
    print("URL is {0}".format(urlname))
    nameoffile = request.form['Name']
    print("Image name {0}".format(nameoffile))
    nameoffile = nameoffile+".jpg"
    urllib.request.urlretrieve(urlname, filename=nameoffile)
    BUCKET = "test-codebuild-deploy"
    Key = nameoffile
    outPutname = nameoffile
    s3 = boto3.client('s3')
    s3.upload_file(Key,BUCKET,outPutname)
    date_today =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mydb = mysql.connector.connect(
    host="xxxx",
    user="xxxx",
    passwd="xxxx",
    database="test1")
    mycursor = mydb.cursor()
    sql = "INSERT INTO s3dataa ( URL, name, path, date) VALUES (%s, %s, %s, %s)"
    val = ( urlname, nameoffile, BUCKET+Key , date_today)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Image uploaded to S3")
    return home()



@app.route('/get_data', methods=['POST'])
def get_data():
    print ("done")
    my_bucket = s3.Bucket('test-codebuild-deploy')
    assets = list()
    for obj in my_bucket.objects.all():
        assets.append((obj.bucket_name, obj.key))
    return json.dumps(assets)

if __name__ == '__main__':
     app.run(host='0.0.0.0',port=5002)
