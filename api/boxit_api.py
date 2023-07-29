from flask import render_template, request
from . import boxitApi
from dal.gameroom import get_roomdetails
from utils.database_config import mongodb

@boxitApi.route("/")
def home():
    return render_template('boxit/home.html')

@boxitApi.route("/local")
def local():
    return render_template('boxit/local.html')

@boxitApi.route("/multiplayer")
def multiplayer():
    return render_template('boxit/multiplayer.html')
    
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
            return render_template('boxit/waitinglobby.html', roomid = roomid)
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