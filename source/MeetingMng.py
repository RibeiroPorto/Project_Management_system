from source.database import db_session
from source.DBMng import Meeting


def Schedule_meeting(Scheduler_id, Invitee_id,Project,DateTime, Description,Status="Pending" ):
    U = Meeting( Scheduler_id, Invitee_id,Project,DateTime, Description,Status )
    db_session.add(U)
    db_session.commit()
    return
def ScheduledMeetings(user):
    meetings = Meeting.query.filter_by(Scheduler_id=user)
    
    return meetings

def InviteeMeetings(user):
    meetings = Meeting.query.filter_by(Invitee_id=user)
    
    return meetings