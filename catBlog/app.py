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


"""NOTE S
This can also be done with fingerprinting as well. 
essentially, "the dangers of dynamic content" enable adversaries to show content tailored to their user
Think of it like how facebook shows you adds based on the things you're interested in,
but now it is, instead, a website that tailor's its content to the user. 
If we can extrapolate things about a person, we can show them this content. 
This does, of course, have its downsides. There is nothing from stopping law enforcement from
impersonating a nair-do-well. so then it is, therefore, most imperitive that the 'advertising' 
be done on a suitable platform such that it draws the attention of other adversaries and not
the ire of law enforcement. 
That said, law enforcement is very likely to know about these things anyway. 
Also as far as I can tell there is no research on this topic.
Why is that <FIND REASONS>. 
either there is some reason/thing that makes this not appealing or 
there is another option that is better suited for this task
or this approach is fundementally flawed in some way. 
Now what would be 'cool' is if someone developed a program that enabled this type of 'hidden content' 
on an average website... It is defintely doable. This demo took me 3 days to put together. 
Think of how much more time and effort adversaries are putting into their work 
and how much more sophisticated their approach could be. """

# @app.route('/frombutton')
# def frombutton():
    
#     #print("request form from button!",request.form)
#     if "moarDogs" in request.args:
#         print("MOAR DOGS REQUESTED")
#         return redirect(url_for("dogs"))
#     else:
#         return render_template("index.html", showImgs=False)
    

    
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
    return render_template("index.html", showImgs=False,imgName="", showBad=False)
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
    return render_template("index.html", showImgs=True,images=imgout, showBad=False)

@app.route('/friendlyRedirect', methods=['GET','POST'])
def friendlyRedirect():
    form = request.form
    print("/friendlyRedirect", form)
    """TODO?"""
    return render_template("index.html", showImgs=False, showBad=False)

def getValidToken():
    #token generation logic here.
    return "aaabbbccc"    

@app.route("/readCookie")
def readCookie():
    print("reading cookies")
    token = request.cookies.get('token')
    if(tokenIsValid(token)):
        imgout = getBadImages()
        return render_template("index.html", showImgs=True,images=imgout, showBad=True)
    else:
        return render_template("index.html", showImgs=False, showBad=False)
    
def isValidUser(user):
    """method for determining if a user can see bad content or not
    Could be a shared database or a file in the control of this server"""
    return True

@app.route("/loginCookie")
def loginCookie():
    print("reading coologinCookiekies")
    user = request.cookies.get('username')
    if isValidUser(user):
        imgout = getBadImages()
        return render_template("index.html", showImgs=True,images=imgout, showBad=True)
    else:
        return render_template("index.html", showImgs=False, showBad=False)
    

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
        return render_template("index.html", showImgs=True,images=imgout, showBad=True)
    else:
        return render_template("index.html", showImgs=False, showBad=False)

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

    return render_template("index.html", showImgs=True,images=imgout, showBad=True)

def tokenIsValid(token):
    if getValidToken() == token:
        return True 
    else:
        return False

def getBadImages():
    imgs = os.listdir(f"{os.getcwd()}/static/evil")
    imgout = []
    for img in imgs:
        imgout.append("static/evil/"+img)
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
            return render_template("index.html", showImgs=True,images=imgout, showBad=True)
        else:
            return render_template("index.html", showImgs=False, showBad=False)
            
    elif request.method == "GET":
        print("requestform friendly token ", request.form)
        isFriendly = request.args.get('isFriendly')
        token = request.args.get('token')
        if isFriendly and token == getValidToken():
            imgout=getBadImages()
            return render_template("index.html", showImgs=True,images=imgout, showBad=True)
        else:
            return render_template("index.html", showImgs=False, showBad=False)
    else:
        return render_template("index.html", showImgs=False, showBad=False)
    

@app.route('/freindlyReferrerExample', methods=['GET','POST'])
def freindlyReferrerExample():
    ref = request.referrer
    if ref == None:
        return render_template("index.html", showImgs=False,imgName="", showBad=False)
    else:
        if(isFriendly(ref)):
            imgout = getBadImages()
            return render_template("index.html", showImgs=True,images=imgout, showBad=True)
        else:
            return render_template("index.html", showImgs=False,imgName="", showBad=False)

@app.route('/totalySafeLink', methods=['GET','POST'])
def urlExploit():
    #whether or not to exploit the target goes here
    exploit = 1

    if exploit:
        return redirect("http://evil.blog.com/urlExploit")
    else:
        return redirect("http://cat.blog.com")


if __name__ == '__main__':
    # NOTE: DEPLOYMENT, debug needs to be turned off
    app.run(host='0.0.0.0', port=8000, debug=True)