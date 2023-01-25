import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Falta documentar

cred = credentials.Certificate("CERTIFICADO")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'URL'
})

def replaceData(path, data):
    ref = db.reference(path)
    ref.set(data)


def saveData(path, data):
    ref = db.reference(path)
    ref.push(data)


def getData(path, puuid):
    ref = db.reference(path).order_by_key().equal_to(puuid).limit_to_last(1)
    return ref.get()

def getUsuarios():
    ref = db.reference('usuario')
    return ref.get()

def addGame(path, gameId):
    ref = db.reference(path)
    ref.set(gameId)

def deleteGame(path):
    ref = db.reference(path)
    ref.delete();

def getGames():
    ref = db.reference('game').order_by_value()
    return ref.get()
