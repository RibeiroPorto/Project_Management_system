from flask import Flask, url_for,request, redirect, render_template, session
from markupsafe import escape
from source.database import init_db
from source.database import db_session
from source.UserMng import createUser, UserLogin, showAllUsers
from source.ProjectMng import CreateProject, showAllProjects, DeleteProject, showProject
from source.ProjectMng import  CreateTask, showAllTasks,DeleteTask, CompleteTask, UncompleteTask
from source.MeetingMng import Schedule_meeting,ScheduledMeetings ,InviteeMeetings
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
            session['userID']=login.id
            
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
    
    if "project" in session:
        project=[session['project'],session['project_ProductCode'],session['project_Description'],session['project_Contacts']]
        return render_template('desktop.html', project=project, projects=showAllProjects())
    return render_template('desktop.html', project=False, projects=showAllProjects())

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

@app.route('/open_project/<projectID>')
def open_project(projectID):
    session['project_id']=showProject(projectID).id
    session["project"]=showProject(projectID).projectID
    session["project_ProductCode"]=showProject(projectID).ProductCode
    
    session["project_Description"]=showProject(projectID).Description
    session["project_Contacts"]=showProject(projectID).Contacts
    return redirect(url_for('desktop'))
    
@app.route('/close_project')
def close_project():
    if 'project' in session:
        session.pop("project")
    return redirect(url_for('desktop'))

@app.route('/task_management', methods=['GET','POST'])
def task_management():
    if request.method=='POST':
        task_name = request.form['taskName']
        task_description = request.form['taskDescription']
        CreateTask(session['project_id'],task_name,task_description)
    
    tasks=showAllTasks(session['project_id'])
    print(tasks[0].Status)
    project=[session['project'],session['project_ProductCode'],session['project_Description'],session['project_Contacts']]
    return  render_template('taskMng.html', tasks=tasks,project=project)

@app.route('/delete_task/<taskID>')
def delete_task(taskID):
    print(taskID)
    DeleteTask(taskID)
    return redirect(url_for('task_management'))

@app.route('/complete_task/<taskID>')
def complete_task(taskID):
    print(taskID)
    CompleteTask(taskID)
    return redirect(url_for('task_management'))

@app.route('/uncomplete_task/<taskID>')
def uncomplete_task(taskID):
    print(taskID)
    UncompleteTask(taskID)
    
    return redirect(url_for('task_management'))


################################################################33
#Meeting Scheduling
@app.route("/meeting", methods=['GET','POST'])
def meeting():
    if request.method=="POST":
        scheduler=session['userID']
        invitee= request.form['user']
        project=request.form['project']
        dateTime = request.form['meetingDateTime']
        description = request.form['meetingDescription']
        print(scheduler,invitee,project,dateTime,description)
        Schedule_meeting(scheduler, invitee,project,dateTime, description)
       # Schedule_meeting()
    Users= showAllUsers()
    Projects= showAllProjects()
    scheduled=ScheduledMeetings(session['userID'])
    invite=InviteeMeetings(session['userID'])

    return render_template('meeting.html',users=Users, projects=Projects, scheduled=scheduled, invite=invite)

if __name__=="__main__":
    init_db()
    app.run(debug=True,host="0.0.0.0")

    