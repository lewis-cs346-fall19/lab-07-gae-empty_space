# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import logging

import cgi
import cgitb
import MySQLdb
#import pymysql
import passwords
import os
import random

from flask import Flask, request, render_template, url_for, redirect, make_response,json


app = Flask(__name__)
#t = self.request.cookies.get("cookie_name")
#print(t)

@app.route('/')
def hello():
    conn = MySQLdb.connect(unix_socket = "/cloudsql/gaeproj:us-central1:kirch-data",user = passwords.SQL_USER,passwd = passwords.SQL_PASSWD,db = 'cookies')

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM sessionz;')

    results = cursor.fetchall()

    print("Here's the Results:")
    print(results)

    cursor.close()
    conn.close()

    #response = make_response()
   
    #response.set_cookie("cookie_name", "12367", max_age=1800)

    t = request.cookies.get("cookie_name_8")

    print(t)

    try:
        u = request.values['username']
    except:
        u = ''

    try:
        j = request.values['inc']
    except:
        j = 0

    print(j)

    if(t is None):
        response = make_response(render_template("form.html"))
        id = "%032x" % random.getrandbits(128)
        sid = str(id)
        response.set_cookie("cookie_name_8", sid, max_age=1800)
        conn = MySQLdb.connect(unix_socket = "/cloudsql/gaeproj:us-central1:kirch-data",user = passwords.SQL_USER,passwd = passwords.SQL_PASSWD,db = 'cookies')

        cursor = conn.cursor()

        cursor.execute('INSERT INTO sessionz(session_id) VALUES (%s);',(id,))
        print(sid)
    
        conn.commit()

        cursor.close()
        conn.close()


        return response
        #return render_template("basic.html")
    else:
        if( u != ''):
            conn = MySQLdb.connect(unix_socket = "/cloudsql/gaeproj:us-central1:kirch-data",user = passwords.SQL_USER,passwd = passwords.SQL_PASSWD,db = 'cookies')

            cursor = conn.cursor()

            cursor.execute('UPDATE sessionz SET username=%s WHERE session_id=%s;',(u,t))
        
    
            conn.commit()

            cursor.close()
            conn.close()

            conn = MySQLdb.connect(unix_socket = "/cloudsql/gaeproj:us-central1:kirch-data",user = passwords.SQL_USER,passwd = passwords.SQL_PASSWD,db = 'cookies')

            cursor = conn.cursor()

            cursor.execute('INSERT INTO Inc(username,val) VALUES(%s,1);',(u,))
        
    
            conn.commit()

            cursor.close()
            conn.close()


            return render_template("increment.html",u=1,n=u)
        if(j !=0):
            
            conn = MySQLdb.connect(unix_socket = "/cloudsql/gaeproj:us-central1:kirch-data",user = passwords.SQL_USER,passwd = passwords.SQL_PASSWD,db = 'cookies')

            cursor = conn.cursor()

            

            cursor.execute('SELECT username FROM sessionz WHERE session_id=%s;',(t,))
        
            results = cursor.fetchall()

            us=results[0][0]
            print(us)
    
            conn.commit()

            cursor.close()
            conn.close()
            
            conn = MySQLdb.connect(unix_socket = "/cloudsql/gaeproj:us-central1:kirch-data",user = passwords.SQL_USER,passwd = passwords.SQL_PASSWD,db = 'cookies')

            cursor = conn.cursor()

            

            cursor.execute('SELECT val FROM Inc WHERE username=%s;',(us,))
        

            results = cursor.fetchall()

            v=results[0][0]
            print(v)

            cursor.execute('UPDATE Inc SET val=%s WHERE username=%s;',(v+1,us))
    
            conn.commit()

            cursor.close()
            conn.close()
            return render_template("increment.html", u=v+1, n=us)
        else:

            conn = MySQLdb.connect(unix_socket = "/cloudsql/gaeproj:us-central1:kirch-data",user = passwords.SQL_USER,passwd = passwords.SQL_PASSWD,db = 'cookies')

            cursor = conn.cursor()

            

            cursor.execute('SELECT username FROM sessionz WHERE session_id=%s;',(t,))
        
            results = cursor.fetchall()

            us=results[0][0]
            print(us)
    
            conn.commit()

            cursor.close()
            conn.close()


            conn = MySQLdb.connect(unix_socket = "/cloudsql/gaeproj:us-central1:kirch-data",user = passwords.SQL_USER,passwd = passwords.SQL_PASSWD,db = 'cookies')

            cursor = conn.cursor()

            

            cursor.execute('SELECT val FROM Inc WHERE username=%s;',(us,))
        

            results = cursor.fetchall()

            v=results[0][0]
            print(v)
            
            #cursor.execute('UPDATE Inc SET val=%s WHERE username=%s;',(v+1,us))


            conn.commit()

            cursor.close()
            conn.close()

            return render_template("increment.html", u=v, n=us)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]
