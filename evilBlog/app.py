from flask import Flask, redirect, request, url_for, render_template, session, abort,make_response
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
    app.wsgi_app, x_for=3, x_proto=3, x_host=3, x_prefix=3
)

def getValidToken():
    #token generation logic here.
    return "aaabbbccc"    


@app.route('/')
def index():    
    return render_template("index.html", showImgs=False,imgName="",token=getValidToken())

@app.route('/cats')
def cats():
    imgName  = 'cat'
    imgs = os.listdir(f"{os.getcwd()}/static/cats")
    imgout = []
    for img in imgs:
        imgout.append("/static/cats/"+img)
    print(imgs)
    return render_template("index.html", showImgs=True,images=imgout)



@app.route("/login")
def login():
    return render_template("login.html")


def isValidUser(username,password):
    return True

@app.route("/login2", methods=['POST'])
def login2():
    username = request.form['username']
    password = request.form['password']
    if(isValidUser(username,password)):
        #return render_template("authenticated.html", user=username)
        resp = make_response(render_template('authenticated.html'))
        resp.set_cookie('username',username,domain="blog.com")
        return(resp)
    else:
        return render_template("authenticated.html", user="Not a valid user")

@app.route("/giveMeCookie")
def giveMeCookie():
    """Sets the obscure token in the user's cookies."""
    resp = make_response(render_template('giveMeCookie.html'))
    #resp.set_cookie('token', getValidToken(),domain="blog.com")
    resp.set_cookie('token', getValidToken())
    return(resp)


@app.route("/friendlyRedirectClientToken", methods=['POST'])
def friendlyRedirectClientToken():
    print("friendly redirect function called")
    token = request.form.get('token')
    return(redirect(f"http://cat.blog.com/friendlyServerClientToken?token={token}&isFriendly=True",code=302))
    
@app.route("/friendlyRedirectServerToken", methods=['POST'])
def friendlyRedirectServerToken():
    print("friendly redirect function called")
    token = getValidToken()
    return(redirect(f"http://cat.blog.com/friendlyServerClientToken?token={token}&isFriendly=True",code=302))

if __name__ == '__main__':
    

    # NOTE: DEPLOYMENT, debug needs to be turned off
    app.run(host='0.0.0.0', port=8001, debug=True)