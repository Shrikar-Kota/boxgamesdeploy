from flask_socketio import emit, join_room, rooms
from random import randrange
from datetime import datetime, timezone

from . import socketio
from dal.gameroom import get_all_documents, create_new_room, get_roomdetails, delete_room_details, update_room_details

@socketio.on('createroom', namespace = '/boxit')
def createroom():
    previds = [document["_id"] for document in get_all_documents()]
    newid = randrange(10**6, 10**7)
    while newid in previds:
        newid = randrange(10**6, 10**7)
    gamedetails = {
        "_id": newid,
        "playercount": 1,
        "starttime": int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
    }
    try:
        create_new_room(gamedetails)
        emit('roomcreated', {'roomid': newid}) 
    except:
        emit('roomecreationerror')
        
@socketio.on('findroom', namespace = '/boxit')
def findroom(payload):
    roomid = payload['roomid']
    room_details = get_roomdetails(roomid)
    if room_details is not None and room_details["playercount"] != 2:
        room_details["playercount"] = 2
        update_room_details(roomid, room_details)
        emit('roomfound', {'roomid': roomid})
        emit('opponentjoined', {'roomid': roomid}, to = str(roomid)+"WL")
    else:
        emit('roomnotfounderror')
    
@socketio.on('joinroom', namespace = '/boxit')
def joinroom(payload):
    roomid = payload['roomid']
    room_details = get_roomdetails(roomid)
    if room_details is None:
        emit("roomnotfounderror")
    else:
        join_room(roomid)
    
@socketio.on('joinwaitinglobby', namespace = '/boxit')
def joinwaitinglobby(payload):
    roomid = payload['roomid']
    room_details = get_roomdetails(roomid)
    if room_details is None:
        emit("roomnotfounderror")
    else:
        join_room(str(roomid)+"WL")
    
@socketio.on('killroom', namespace = '/boxit')
def killroom(payload):
    roomid = payload["roomid"]
    room_details = get_roomdetails(roomid)
    if room_details is not None and room_details["playercount"] != 2:
        delete_room_details(roomid)
    
@socketio.on("gamerestartrequestsent", namespace = "/boxit")
def gamerestartappealcreated(payload):
    roomid = payload["roomid"]
    room_details = get_roomdetails(roomid)
    if room_details is not None:
        emit("gamerestartrequested", room = roomid, include_self = False)
        
@socketio.on("gamerestartacceptsent", namespace = "/boxit")
def gamerestartappealaccepted(payload):
    roomid = payload["roomid"]
    room_details = get_roomdetails(roomid)
    if room_details is not None:
        emit("gamerestartaccepted", room = roomid, include_self = False)
        
@socketio.on("gamerestartdeclinesent", namespace = "/boxit")
def gamerestartappealdeclined(payload):
    roomid = payload["roomid"]
    room_details = get_roomdetails(roomid)
    if room_details is not None:
        emit("gamerestartdeclined", room = roomid, include_self = False)
    
@socketio.on("moveplayed", namespace = "/boxit")
def moveplayed(payload):
    roomid = payload["roomid"]
    room_details = get_roomdetails(roomid)
    if room_details is not None:
        emit("opponentmoveplayed", payload, room = roomid, include_self = False)
        
@socketio.on("timelimitexceededtrigger", namespace = "/boxit")
def timelimitexceeded(payload):
    roomid = payload["roomid"]
    room_details = get_roomdetails(roomid)
    if room_details is not None:
        emit("timelimitexceeded", room = roomid, include_self = True)
        
@socketio.on("resetmovetimerevent", namespace = "/boxit")
def resetmovetimer(payload):
    roomid = payload["roomid"]
    room_details = get_roomdetails(roomid)
    if room_details is not None:
        emit("resetmovetimer", room = roomid, include_self = True)
    
@socketio.on("newmessagesent", namespace = "/boxit")
def newmessagesent(payload):
    roomid = payload["roomid"]
    room_details = get_roomdetails(roomid)
    print(room_details)
    if room_details is not None:
        emit("newmessagereceived", payload, room = roomid, include_self = False)
        
@socketio.on('disconnect', namespace = '/boxit')
def disconnect():
    room_details = None
    for roomid in rooms():
        if type(roomid) == int:
            room_details = get_roomdetails(roomid)
            break
    if room_details is not None:
        if room_details["playercount"] == 2:
            emit("opponentdisconnected", room = room_details['_id'])
            delete_room_details(room_details["_id"])