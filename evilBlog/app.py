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