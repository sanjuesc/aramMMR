import numpy as np
import firebase
from riotwatcher import LolWatcher, ApiError
from datetime import timedelta, datetime
import mysql.connector

#Falta documentar


def main():
    lol_watcher = LolWatcher('API-KEY')
    my_region = 'euw1'
    #Desde ayer a hoy
    inicio = np.compat.long((datetime.now() - timedelta(days=1)).timestamp())
    final = np.compat.long((datetime.now()).timestamp())
    for k in firebase.getUsuarios():
        historial = lol_watcher.match.matchlist_by_puuid(my_region, k, queue=450, start_time=inicio,
                                                         end_time=final)
        for elem in reversed(historial):
            mydb = mysql.connector.connect(
                host="HOST",
                user="USER",
                password="PASSWORD",
                database="DATABASE"
            )
            cursor = mydb.cursor(buffered=True)
            sql = ("SELECT * FROM games WHERE matchId = %s")
            cursor.execute(sql, (elem,))
            if cursor.rowcount == 0:
                start = lol_watcher.match.by_id(my_region, elem)['info']['gameCreation']
                firebase.addGame('game/'+elem, start)
            else:
                pass
            cursor.close()
            mydb.close()




if __name__ == '__main__':
    main()
