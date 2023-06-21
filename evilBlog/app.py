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
    resp.set_cookie('token', getValidToken(),domain="blog.com")
    #resp.set_cookie('token', getValidToken())
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


@app.route('/urlExploit', methods=['GET','POST'])
def urlExploit():
    return render_template("exploit.html")
    



@app.route('/yubi')
def yubi():
    return render_template("yubi.html")

def getYubiClientId():
    with open('secrets.txt', "r") as f:
        client_id = f.readline()
    return client_id.strip('\n')


from secrets import token_urlsafe
from requests import request as req
def isValidUserOTP(username, password, otp):
    if isValidUser(username,password):
        #dev override. Just accept this as true
        #this would NEVER be done in production.
        #if you dont have a yubikey you can just set this to always return TRUE for the yubi part. 

        if(otp == "OVERRIDE"):
            return True
        #nonce has a length requirement from yubi. 
        #if it is not within the valid range (i think its 26-40) you will get a MISSING_PARAMATER status back
        #token_urlsafe gives us _ and - which yubi does not like, so get rid of them. 
        nonce = token_urlsafe()[:28].replace("_",'a').replace('-','b')

        #get the client_id from your secret file
        client_id = getYubiClientId()
        #URL we want to send the request to. 
        print("sending ",client_id, nonce, otp, " to yubikey")
        yubiUrl = f"https://api.yubico.com/wsapi/2.0/verify?id={client_id}&nonce={nonce}&otp={otp}"
        response = req(url=yubiUrl,method="POST")
        
        #response.status_code will always be 200 even if the thing is replayed
        # instead convert the response we get to a dictionary s
        # if the values change possition in the future the values we get back should still be the same. 
        parsed = response.text.split('\r\n')
        responseDict = {}
        for line in parsed:
            #skip empty lines
            if line != "":
                values = line.split('=')
                responseDict[values[0]]=values[1]
                
        #debug print statments
        print(parsed, len(parsed))
        print(responseDict)
        if responseDict['status'] == 'REPLAYED_REQUEST':
            print("DUPLICATE OTP REQUEST THIS IS BAD")
            return False
        elif responseDict['status'] == 'OK':
            return True
        else:
            return False

        
    else:
        return False

@app.route('/yubilogin', methods=['POST'])
def yubilogin():
    #print(request.form)
    username = request.form['username']
    password = request.form['password']
    otp = request.form['otp']
    if(isValidUserOTP(username,password,otp)):
        #for now <<TODO>
        resp = make_response(render_template('authenticated.html',loggedInYubi=True))
        resp.set_cookie('username',username,domain="blog.com")
        return(resp)
    else:
        return render_template("authenticated.html", user="Not a valid user")
    


if __name__ == '__main__':
    

    # NOTE: DEPLOYMENT, debug needs to be turned off
    app.run(host='0.0.0.0', port=8001, debug=True)