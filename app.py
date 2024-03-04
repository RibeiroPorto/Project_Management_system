from flask import Flask, url_for,request, redirect, render_template, session
from markupsafe import escape
from source.database import init_db
from source.database import db_session
from source.UserMng import createUser, UserLogin
from source.ProjectMng import CreateProject, showAllProjects, DeleteProject
from config import secret_key

app=Flask(__name__)
app.config['SECRET_KEY'] = secret_key




@app.route("/")
def index():
    
    return render_template('index.html')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/login', methods=['GET','POST'])
def Login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        login = UserLogin(username,password)
        print(login.name)
        if login==None:
            print("login")
            
        else:
            session['user']=login.name
            session['role']=login.role
            
            return redirect(url_for('desktop'))
    return render_template('login.html')

@app.route('/logoff', methods=['GET','POST'])
def Logoff():
    session.pop('user')
    return redirect(url_for("index"))

@app.route('/Create_user', methods=['GET','POST'])
def Create_user():
    if request.method=="POST":
        username=request.form['username']
        email=request.form['username']
        password=request.form['password']
        role=request.form['role']
        registry=request.form['registry']

        createUser(username,email,password,role,registry)
        redirect(url_for('Login'))
    return render_template('createUser.html')

@app.route('/desktop')
def desktop():
    if not 'user' in session:
        return redirect(url_for('index'))
    
    return render_template('desktop.html', user=session['user'], projects=showAllProjects())

@app.route('/project', methods=['GET','POST'])
def project_info():
    if request.method=="POST":
        projectID=request.form['projectId']
        ProductCode=request.form['productCode']
        Description=request.form['description']
        Contacts=request.form['costumerContacts']

        CreateProject(projectID,ProductCode,Description,Contacts)
        return redirect(url_for('desktop'))
    return render_template("project_manage.html")

@app.route('/delete_project/<projectID>')
def delete_project(projectID):

    print(projectID)
    DeleteProject(projectID)
    return redirect(url_for('desktop'))

if __name__=="__main__":
    init_db()
    app.run(debug=True,host="0.0.0.0")

    