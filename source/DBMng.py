from sqlalchemy import Column, Integer, String, Text
from source.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    email = Column(String(120), unique=False)
    passwd = Column(String(20), unique=False)
    role = Column(String(15), unique=False)
    registry = Column(String(10), unique=False)

    def __init__(self, name=None, email=None, passwd=None, role=None, registry=None):
        self.name = name
        self.email = email
        self.passwd = passwd
        self.role = role
        self.registry = registry

    def __repr__(self):

        return self.name, self.email,self.role,self.registry
    
class Projects(Base):
    __tablename__ = 'Projects'
    id = Column(Integer, primary_key=True)
    projectID = Column(String(50), unique=False)
    ProductCode = Column(String(120), unique=False)
    Description = Column(Text, unique=False)
    Contacts = Column(String(20), unique=False)

    def __init__(self, projectID=None, ProductCode=None, Description=None, Contacts=None):
        self.projectID = projectID
        self.ProductCode = ProductCode
        self.Description = Description
        self.Contacts = Contacts

    def __repr__(self):

        return self.id,self.projectID, self.ProductCode,self.Description,self.Contacts
    
class Tasks(Base):
    __tablename__ = 'Task'
    id = Column(Integer, primary_key=True)
    project_ID = Column(Integer, unique=False)
    Name=    Description = Column(String(20), unique=False)
    Description = Column(Text, unique=False)
    Status =Column(String(20), unique=False)

    def __init__(self, projec_tID=None, Name=None, Description=None,Status=None ):
        self.project_ID = projec_tID
        self.Description = Description
        self.Status = Status
        self.Name = Name

    def __repr__(self):

        return self.id,self.Name,self.project_ID,self.Description,self.Status
    