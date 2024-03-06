from source.database import db_session
from source.DBMng import Meeting


def Schedule_meeting(Scheduler,Scheduler_id, Invitee_id,Invitee,Project,DateTime, Description, Status="Pending"):
    U = Meeting( Scheduler, Scheduler_id, Invitee_id,Invitee,Project,DateTime, Description,Status )
    db_session.add(U)
    db_session.commit()
    return
def ScheduledMeetings(user):
    meetings = Meeting.query.filter_by(Scheduler_id=user).all()
    
    return meetings

def InviteeMeetings(user):
    meetings = Meeting.query.filter_by(Invitee_id=user).all()
    
    return meetings

def DeletMeetings(meet_id):
    U = Meeting.query.filter_by(id=meet_id).first()
    db_session.delete(U)
    
    db_session.commit()
    return

def ChangeMeetingsStatus(meet_id,Status):
    Status_dic={1:"Pending",2:"Accepted",3:"Rejected"}
    
    U = Meeting.query.filter_by(id=meet_id).first()
    U.Status=Status_dic[Status]
    
    db_session.commit()
    return
