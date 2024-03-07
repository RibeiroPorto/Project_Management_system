from flask import Flask, url_for,request, redirect, render_template, session
from markupsafe import escape
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from source.database import init_db
from source.database import db_session
from source.UserMng import createUser, UserLogin, showAllUsers, Username
from source.ProjectMng import CreateProject, showAllProjects, DeleteProject, showProject
from source.ProjectMng import  CreateTask, showAllTasks,DeleteTask, CompleteTask, UncompleteTask
from source.MeetingMng import Schedule_meeting,ScheduledMeetings ,InviteeMeetings, DeletMeetings, ChangeMeetingsStatus
from config import secret_key

app=Flask(__name__)
app.config['SECRET_KEY'] = secret_key


@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for('desktop'))
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
        session.pop("project_id")
        session.pop("project_ProductCode")
        session.pop('project_Description')
        session.pop('project_Contacts')

    return redirect(url_for('desktop'))

@app.route('/task_management', methods=['GET','POST'])
def task_management():
    if request.method=='POST':
        task_name = request.form['taskName']
        task_description = request.form['taskDescription']
        CreateTask(session['project_id'],task_name,task_description)
    
    tasks=showAllTasks(session['project_id'])
    project=[session['project'],session['project_ProductCode'],session['project_Description'],session['project_Contacts']]
    return  render_template('taskMng.html', tasks=tasks,project=project)

@app.route('/delete_task/<taskID>')
def delete_task(taskID):
    DeleteTask(taskID)

    return redirect(url_for('task_management'))

@app.route('/complete_task/<taskID>')
def complete_task(taskID):
    CompleteTask(taskID)
    return redirect(url_for('task_management'))

@app.route('/uncomplete_task/<taskID>')
def uncomplete_task(taskID):
    UncompleteTask(taskID)
    
    return redirect(url_for('task_management'))




################################################################33
#Meeting Scheduling
@app.route("/meeting", methods=['GET','POST'])
def meeting():
    if request.method=="POST":
        scheduler_id=session['userID']
        scheduler=session['user']
        invitee_id= request.form['user']
        invitee=Username(request.form['user'])
        project=request.form['project']
        dateTime = request.form['meetingDateTime']
        description = request.form['meetingDescription']
        try:
            dt_obj = datetime.fromisoformat(dateTime)
        except:
            dt_obj=""
        Schedule_meeting(scheduler,scheduler_id, invitee_id,invitee,project,dt_obj, description)
       # Schedule_meeting()
    Users= showAllUsers()
    Projects= showAllProjects()
    scheduled=ScheduledMeetings(session['userID'])
    invite=InviteeMeetings(session['userID'])
    return render_template('meeting.html',users=Users, projects=Projects, scheduled=scheduled, invite=invite)

@app.route("/delete_meeting/<meet_id>")
def delete_meeting(meet_id):
    DeletMeetings(meet_id)
    return redirect(url_for('meeting'))

@app.route("/accept_meeting/<meet_id>")
def accept_meeting(meet_id):
    ChangeMeetingsStatus(meet_id,2)
    return redirect(url_for('meeting'))

@app.route("/reject_meeting/<meet_id>")
def reject_meeting(meet_id):
    
    ChangeMeetingsStatus(meet_id,3)
    return redirect(url_for('meeting'))

#########################################################
# Progress Tracking

@app.route('/progress')
def progress():
    if 'project_id' in session:
        tasks=showAllTasks(session['project_id'])
        project=session['project']
        todo=0
        done=0
        onhold=0
        for task in tasks:
            if task.Status=="Done":
                done+=1
            if task.Status=="To Do":
                todo+=1
            if task.Status=="On Hold":
                onhold+=1
        # Generate the pie chart
        labels = ["Done","To Do", "On Hold"]
        sizes = [todo, done, onhold]
        if todo==0 and done==0 and onhold==0:
            return render_template('progressTracking.html',tasks=[{'tasks':tasks, 'project':project,"img":url_for('static', filename='media/image.png')}])
        explode = (0, 0, 0)  # explode the 2nd slice
        
        colors = ['Yellow', 'green', 'grey']  # Define custom colors
        fig, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90,  textprops={'fontsize': 20},colors=colors)
        ax.axis('equal')  
        plt.tight_layout()

        # Save the pie chart as PNG image in memory
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        # Encode the PNG image as base64

        # Encode the PNG image as base64
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        
        #" data:image/png;base64,{{ img }}"
        print(todo,done,onhold)
        return render_template('progressTracking.html',tasks=[{'tasks':tasks, 'project':project,"img":f" data:image/png;base64,{ img_base64 }"}])
    else:
        projects=showAllProjects()
        project_data_list=[]
        for project in projects:
            tasks=showAllTasks(project.id)
            project=project.projectID
            todo=0
            done=0
            onhold=0
            for task in tasks:
                if task.Status=="Done":
                    done+=1
                if task.Status=="To Do":
                    todo+=1
                if task.Status=="On Hold":
                    onhold+=1
            # Generate the pie chart
            labels = ["Done","To Do", "On Hold"]
            sizes = [todo, done, onhold]
            if todo==0 and done==0 and onhold==0:
                project_data= {"tasks":tasks,"project":project,"img":url_for('static', filename='media/image.png')}
                project_data_list.append(project_data)
                continue
            explode = (0, 0, 0)  # explode the 2nd slice
            
            colors = ['Yellow', 'green', 'grey']  # Define custom colors
            fig, ax = plt.subplots()
            ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90,  textprops={'fontsize': 20},colors=colors)
            ax.axis('equal')  
            plt.tight_layout()

            # Save the pie chart as PNG image in memory
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)

            # Encode the PNG image as base64

            # Encode the PNG image as base64
            img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
            project_data= {"tasks":tasks,"project":project,"img":f" data:image/png;base64,{ img_base64 }"}
            project_data_list.append(project_data)
        return render_template('progressTracking.html',tasks=project_data_list)

    return render_template('progressTracking.html')

if __name__=="__main__":
    init_db()
    app.run(debug=True,host="0.0.0.0")

    