
from source.database import db_session
from source.DBMng import User

def createUser(user,email,passwd,role,registry):
    U = User(user,email,passwd,role,registry)
    db_session.add(U)
    db_session.commit()


def showAllUsers():
    print('\n')
    return User.query.all()


def UserLogin(user,passwd):
    isUser = User.query.filter_by(name=user,passwd=passwd).first()
    
    return isUser

