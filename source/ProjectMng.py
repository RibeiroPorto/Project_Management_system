
from source.database import db_session
from source.DBMng import Projects, Tasks

def CreateProject(projectID,ProductCode,Description,Contacts):
    U = Projects(projectID,ProductCode,Description,Contacts)
    db_session.add(U)
    db_session.commit()


def showAllProjects():
    return Projects.query.all()
    print('\n')

def DeleteProject(projectID):
    U=Projects.query.filter_by(id=projectID).first()
    db_session.delete(U)
    
    db_session.commit()

def showProject(projectID):
    return  Projects.query.filter_by(id=projectID).first()

#tasks
def CreateTask(project_ID,Name,Description):
    U = Tasks(project_ID,Name,Description,Status="To Do")
    db_session.add(U)
    db_session.commit()


def showAllTasks(project_ID):
    return Tasks.query.filter_by(project_ID=project_ID).all()
    print('\n')
    
def DeleteTask(taskId):
    U=Tasks.query.filter_by(id=taskId).first()
    db_session.delete(U)
    
    db_session.commit()

def CompleteTask(taskID):
    U=Tasks.query.filter_by(id=taskID).first()
    U.Status="Done"
    
    db_session.commit()
def UncompleteTask(taskID):
    U=Tasks.query.filter_by(id=taskID).first()
    U.Status="To Do"
    
    db_session.commit()
