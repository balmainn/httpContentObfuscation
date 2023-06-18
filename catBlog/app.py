from flask import Flask, redirect, request, url_for, render_template, session, abort

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


@app.route('/frombutton')
def frombutton():
    
    #print("request form from button!",request.form)
    if "moarDogs" in request.args:
        print("MOAR DOGS REQUESTED")
        return redirect(url_for("dogs"))
    else:
        return render_template("index.html", showImgs=False)
    

    
def isFriendly(referer):
    ref = str(referer)
    print("ref from frinedly: ", ref)
    lines = []
    with open ("friendly.txt","r") as f:
        line = f.readline().replace("\n","")
        lines.append(line)
    print(lines)    
    if ref in lines:
            print("FRIENDLY SITE FOUND!")
            return True
    print("site is not friendly =(")
    return False
@app.route('/',  methods=['GET','POST'])
def index():    
    return render_template("index.html", showImgs=False,imgName="")
    # ref = request.referrer
    # friendly = False
    # if ref != None:
    #     print("checking if ref is friendly")
    #     friendly = isFriendly(ref)
    # print("friendly result: ", friendly)
    # if not friendly:
    #     return render_template("index.html", showImgs=False,imgName="")
    # else:
    #     return redirect(url_for("freindlyReferrerExample",referer=ref))

@app.route('/cats')
def cats():
    imgName  = 'cat'
    imgs = os.listdir(f"{os.getcwd()}/static/cats")
    imgout = []
    for img in imgs:
        imgout.append("/static/cats/"+img)
    print(imgs)
    return render_template("index.html", showImgs=True,images=imgout)

@app.route('/friendlyRedirect', methods=['GET','POST'])
def friendlyRedirect():
    form = request.form
    print("/friendlyRedirect", form)

    return render_template("index.html", showImgs=False)

def getValidToken():
    #token generation logic here.
    return "aaabbbccc"    

@app.route('/intermidary')
def intermidary(isFriendly=False):
    # print("request from intermediary ", request)
    # if request.args.get('isFriendly') == 'True':
    #     isFriendly = True
    # else:
    #     isFriendly = False
    token = request.args.get('token')
    
    print(token)
    if tokenIsValid(token):
        imgout = getBadImages()
        return render_template("index.html", showImgs=True,images=imgout)
    else:
        return render_template("index.html", showImgs=False)

@app.route('/friendlyServerToken', methods=['POST'])
def friendlyServerToken(isFriendly=False):
    if request.method == "POST":
        print("requestform friendly token ", request.form)
        isFriendly = request.form.get('isFriendly')
        token = request.form.get('token')
        print("friendly: ", isFriendly, " token ", token)
        return "Success", 200, {"token": getValidToken()}
    else:
        return "Not Authorized", 401
    
@app.route("/friendlyServerToken2")
def friendlyServerToken2(isFriendly=False):
    #sever freindly part 2    
    imgout = getBadImages()

    return render_template("index.html", showImgs=True,images=imgout)

def tokenIsValid(token):
    if getValidToken() == token:
        return True 
    else:
        return False

def getBadImages():
    imgs = os.listdir(f"{os.getcwd()}/static/dogs")
    imgout = []
    for img in imgs:
        imgout.append("static/dogs/"+img)
    print(imgout)
    return imgout
    

@app.route('/friendlyServerClientToken', methods=['GET','POST'])
def friendlyServerClientToken(isFriendly=False):
    if request.method == "POST":
        print("requestform friendly token ", request.form)
        isFriendly = request.form.get('isFriendly')
        token = request.form.get('token')
        if isFriendly and token == getValidToken():
            imgout=getBadImages()
            return render_template("index.html", showImgs=True,images=imgout)
            
    else:
        return render_template("index.html", showImgs=False)
    

@app.route('/freindlyReferrerExample', methods=['GET','POST'])
def freindlyReferrerExample():
    ref = request.referrer
    if ref == None:
        return render_template("index.html", showImgs=False,imgName="")
    else:
        if(isFriendly(ref)):
            imgout = getBadImages()
            return render_template("index.html", showImgs=True,images=imgout)
        else:
            return render_template("index.html", showImgs=False,imgName="")



if __name__ == '__main__':
    # NOTE: DEPLOYMENT, debug needs to be turned off
    app.run(host='0.0.0.0', port=8000, debug=True)