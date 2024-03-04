
from source.database import db_session
from source.DBMng import Projects

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