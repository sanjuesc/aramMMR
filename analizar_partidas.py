import firebase
from riotwatcher import LolWatcher, ApiError
import mysql.connector

#Falta documentar

def mmrEquipo(equipo):
    mmr = 0
    for elem in equipo:
        mmr += elem['mmr']
    return mmr / 5


def pVictoriaVS(jugador, equipoRival):
    numero = (equipoRival - jugador) / 400
    p = 1 / (1 + 10 ** numero)
    return p


def simularPartida(equipoA, equipoB, ganador):
    ##no se porque se llama simular partida tbh
    mmrEquipoA = mmrEquipo(equipoA)
    mmrEquipoB = mmrEquipo(equipoB)
    for index, elem in enumerate(equipoA):
        p = pVictoriaVS(elem['mmr'], mmrEquipoB)
        equipoA[index]['p'] = p
    for index, elem in enumerate(equipoB):
        p = pVictoriaVS(elem['mmr'], mmrEquipoA)
        equipoB[index]['p'] = p

    for index, elem in enumerate(equipoA):
        sa = 0
        if ganador == 'A':
            sa = 1
        mmrNuevo = elem['mmr'] + 25 * (sa - elem['p'])
        equipoA[index]['mmr'] = mmrNuevo
        del equipoA[index]['p']
    for index, elem in enumerate(equipoB):
        sa = 0
        if ganador == 'B':
            sa = 1
        mmrNuevo = elem['mmr'] + 25 * (sa - elem['p'])
        equipoB[index]['mmr'] = mmrNuevo
        del equipoB[index]['p']


def main():
    lol_watcher = LolWatcher('API-KEY')
    my_region = 'euw1'
    #TODO: La idea seria cambiarlo a un bucle "infinito" que selecciona el partido mas viejo (el que empezo antes) y lo analiza
    for elem in firebase.getGames():
        equipoA = []
        equipoB = []
        ganador = 'B'
        match = lol_watcher.match.by_id(my_region, elem)
        for index, puiid in enumerate(match['metadata']['participants']):
            usuario = lol_watcher.summoner.by_puuid(my_region, puiid)
            data = firebase.getData('usuario', puiid)
            account = None
            if data:
                account = dict(data)[puiid]
            else:
                account = {
                    'name': usuario['name'],
                    'id': usuario['id'],
                    'accountId': usuario['accountId'],
                    'puuid': usuario['puuid'],
                    'mmr': 1200

                }
                firebase.replaceData('usuario/' + puiid, account)
            if match['info']['participants'][index]['nexusKills'] and index < 5:
                ganador = 'A'
            if index < 5:
                equipoA.append(account)
            else:
                equipoB.append(account)
        simularPartida(equipoA, equipoB, ganador)
        for jugador in equipoA + equipoB:
            firebase.replaceData('usuario/' + jugador['puuid'], jugador)
        mydb = mysql.connector.connect(
            host="HOST",
            user="USER",
            password="PASSWORD",
            database="DATABASE"
        )

        firebase.deleteGame('game/' + elem)
        cursor = mydb.cursor()
        sql = "INSERT INTO games(matchId) VALUES (%s)"
        datos = elem
        cursor.execute(sql, (datos,))
        mydb.commit()
        cursor.close()
        mydb.close()


if __name__ == '__main__':
    main()
