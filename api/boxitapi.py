from flask import render_template, request
from datetime import datetime, timezone

from . import boxitApi
from dal.gameroom import get_roomdetails
from utils.databaseconfig import mongodb

@boxitApi.route("/")
def home():
    return render_template('boxit/home.html')

@boxitApi.route("/localmultiplayer")
def local():
    return render_template('boxit/localmultiplayer.html')

@boxitApi.route("/onlinemultiplayer")
def multiplayer():
    return render_template('boxit/onlinemultiplayer.html')
    
@boxitApi.route("/howtoplay")
def howtoplay():
    return render_template('boxit/howtoplay.html')    
    
@boxitApi.route("/waitinglobby")
def waitinglobby():
    roomid = request.args.get("id")
    if roomid:
        roomid = int(roomid)
        roomdetails = get_roomdetails(roomid, mongodb["gamedata"])
        if roomdetails is not None:
            timeelapsed = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()) - roomdetails['starttime']
            timeleft = 30 - timeelapsed
            if timeleft <= 0:
                timeleft = 0
            return render_template('boxit/onlinewaitinglobby.html', roomid = roomid, timeleft = timeleft)
    return render_template('boxit/home.html')    

@boxitApi.route("/online")
def online():
    roomid = request.args.get("id")
    playername = request.args.get("playername")
    if roomid and playername:
        roomid = int(roomid); playername = int(playername)
        roomdetails = get_roomdetails(roomid, mongodb["gamedata"])
        if roomdetails is not None:
            return render_template('boxit/online.html', roomid = roomid, playername = playername)
    return render_template('boxit/home.html')