from flask import Flask, redirect, request, url_for, render_template, session, abort
import requests as req
import jinja2
#from flask_login import LoginManager, current_user, login_required, login_user, logout_user

#Authentication Testing
import os
#from functools import wraps
#from datetime import timedelta

#there is a bug, all created threads are never rejoined/deleted. 
import threading
environment = jinja2.Environment()
template = environment.from_string("Hello, {{ name }}!")
template.render(name="World")
app = Flask(__name__)
app.config['TESTING'] = True

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=0, x_prefix=0
)

def getRedirectTarget():
    return "http://cat.blog.com"

def getValidToken():
    #token generation logic here.
    return "aaabbbccc"    

@app.route('/')
def index():    
    return render_template("index.html")

@app.route('/redirect')
def redir():    
    target = getRedirectTarget()
    token=getValidToken()
    return(redirect(f"{target}/intermidary?token={token}&isFriendly=True"))


if __name__ == '__main__':
    

    # NOTE: DEPLOYMENT, debug needs to be turned off
    app.run(host='0.0.0.0', port=8002, debug=True)