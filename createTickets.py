

import tawsql
import random


def _countUnusedTickets(cursor, countMap):
    #reset map
    for key in countMap:
        countMap[key] = 0
    #count tickets
    for ticket in cursor:
        key = ticket[tawsql.INITIAL_TIME_INDEX]
        if key in countMap: countMap[key] += 1
        
def _isMapFilled(countMap):
    for key in countMap:
        if countMap[key] < 30: return False
    return True
    
def _fillTicketsInDatabase(countMap):
    for time in countMap:
        count = 30 - countMap[time]
        for x in range(count):
            tawsql.addCode(random.randint(1000, 999999), time)
    
def createAndDumpTickets():
    #clear all used tickets first to clean db and keep it small
    print('Cleaning up database...')
    tawsql.deleteUsedCodes()
    #readd special code if it has been deleted
    tawsql.addCode(215454, 500000)
    print('Database cleaned')
    
    countMap = {tawsql.TEN: 0, 
                    tawsql.FOURTEEN: 0,
                    tawsql.TWENTY: 0,
                    tawsql.THIRTY: 0,
                    tawsql.HOUR: 0 }
    
    print('Filling database ...')
    s = '''SELECT * FROM CODES_TABLE WHERE (TIME!=0 AND TIME=INITIAL_TIME)'''
    cursor = tawsql.conn.execute(s)
    _countUnusedTickets(cursor, countMap)
    print(countMap)
    while not _isMapFilled(countMap):
        _fillTicketsInDatabase(countMap)
        cursor = tawsql.conn.execute(s)
        _countUnusedTickets(cursor, countMap)
    print('Filled database')
    print(countMap)
    print('Dumping tickets ...')
    tawsql.dumpDB('tickets.txt')
    print('Tickets dumped to Desktop folder')
    
    
if __name__ == '__main__':
    createAndDumpTickets()