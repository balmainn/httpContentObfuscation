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



@app.route('/frombutton')
def frombutton():
    
    #print("request form from button!",request.form)
    if "moarDogs" in request.args:
        print("MOAR DOGS REQUESTED")
        return redirect(url_for("dogs"))
    else:
        return render_template("index.html", showImgs=False)
    

    
@app.route('/')
def index():    
    return render_template("index.html", showImgs=False,imgName="")

@app.route('/cats')
def cats():
    imgName  = 'cat'
    imgs = os.listdir(f"{os.getcwd()}/static/cats")
    imgout = []
    for img in imgs:
        imgout.append("/static/cats/"+img)
    print(imgs)
    return render_template("index.html", showImgs=True,images=imgout)

@app.route('/dogs')
def dogs():
    imgName = 'dog'
    imgs = os.listdir(f"{os.getcwd()}/static/dogs")
    imgout = []
    for img in imgs:
        imgout.append("static/dogs/"+img)
    print(imgout)
    return render_template("index.html", showImgs=True,images=imgout)

if __name__ == '__main__':
    

    # NOTE: DEPLOYMENT, debug needs to be turned off
    app.run(host='0.0.0.0', port=8000, debug=True)