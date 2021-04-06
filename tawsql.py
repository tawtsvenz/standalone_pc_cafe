

import os, sqlite3, datetime

#seconds added to first ticket to allow for loading of games and setting up
bonus_time = 200 

#allowed initial times in seconds
TEN = 600 + bonus_time
FOURTEEN = 840 + bonus_time
TWENTY = 1200 + bonus_time
THIRTY = 1800 + bonus_time
HOUR = 3600 + bonus_time
fixed_times = [TEN, FOURTEEN, TWENTY, THIRTY, HOUR]

#indexes of data in database
TICKET_CODE_INDEX = 0
TIME_LEFT_INDEX = 1
INITIAL_TIME_INDEX = 2
DATE_CREATED_INDEX = 3
DATE_SOLD_INDEX = 4

db_name = 'data.db'
script_loc = os.path.abspath(os.path.dirname(__file__))
print(script_loc)
os.chdir(script_loc)
conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES |
                                             sqlite3.PARSE_COLNAMES)
print('database connected')

def createTimeCodesTable():
    conn.execute('''CREATE TABLE IF NOT EXISTS CODES_TABLE
        (TIME_CODE INT PRIMARY KEY NOT NULL,
        TIME INT NOT NULL,
        INITIAL_TIME INT NOT NULL,
        DATE_CREATED TIMESTAMP,
        DATE_SOLD TIMESTAMP);''')
    conn.commit()
        
def addColumnToCodesTable(columnName, columnType):
    s = 'ALTER TABLE CODES_TABLE ADD ? ?'
    data = (columnName,columnType)
    conn.execute(s, data)
    conn.commit()
    
def addCode(time_code, time, timestamp=None):
    '''add the code to database. timestamp will be set to current time if None'''
    #check if code exists
    s = 'SELECT TIME FROM CODES_TABLE WHERE TIME_CODE = ?'
    data_tuple = (time_code, )
    cursor = conn.execute(s, data_tuple)
    if cursor.fetchone() is None:
        #do if time_code doesnt already exist
        if timestamp == None:
            timestamp = datetime.datetime.now()
        s = '''INSERT INTO CODES_TABLE (TIME_CODE, TIME, INITIAL_TIME, DATE_CREATED) \
            VALUES (?, ?, ?, ?)'''
        data_tuple = (time_code, time, time, timestamp)
        conn.execute(s, data_tuple)
        conn.commit()
        return True
    else: return False #failed to add, code already exists
        
def getRow(time_code):
    '''returns None if row doesnt exist'''
    s = 'SELECT * FROM CODES_TABLE WHERE TIME_CODE = ?'
    data_tuple = (time_code,)
    cursor = conn.execute(s, data_tuple)
    return cursor.fetchone()
    
def getAllRows():
    '''returns cursor for all rows in database'''
    s = 'SELECT * FROM CODES_TABLE'
    cursor = conn.execute(s)
    return cursor

def isTicketSold(time_code):
    '''return true if date_sold is not None, false otherwise'''
    ticket = getRow(time_code)
    if ticket == None: return True
    elif ticket[DATE_SOLD_INDEX] == None: return False
    else: return True
    
def updateCode(time_code, new_time, date_created=None, date_sold=None):
    '''update time left on code'''
    s = 'UPDATE CODES_TABLE SET TIME = ? WHERE TIME_CODE=?'
    data_tuple = (new_time, time_code)
    conn.execute(s, data_tuple)
    if date_created != None:
        s = 'UPDATE CODES_TABLE SET DATE_CREATED = ? WHERE TIME_CODE=?'
        data_tuple = (date_created, time_code)
        conn.execute(s, data_tuple)
    if date_sold != None:
        s = 'UPDATE CODES_TABLE SET DATE_SOLD = ? WHERE TIME_CODE=?'
        data_tuple = (date_sold, time_code)
        conn.execute(s, data_tuple)
    conn.commit()
    
def deleteCode(time_code):
    s = 'DELETE FROM CODES_TABLE WHERE TIME_CODE = ?'
    data_tuple = (time_code,)
    conn.execute(s, data_tuple)
    conn.commit()
    
def deleteCodesWithTime(time):
    '''delete codes that have the given initial time'''
    s = 'DELETE FROM CODES_TABLE WHERE INITIAL_TIME = ?'
    data_tuple = (time,)
    conn.execute(s, data_tuple)
    conn.commit()
    
def deleteUsedCodes():
    '''Delete codes that have been used up.
    Delete codes that were bought but not used up in seven days since date of
        buying.
    '''
    #delete exhausted codes
    s = 'DELETE FROM CODES_TABLE WHERE TIME = 0'
    conn.execute(s)
    #delete old codes that were used but not exhausted
    s = "DELETE FROM CODES_TABLE WHERE TIME != INITIAL_TIME AND DATE_SOLD <= DATE('now', '-7 day')"
    conn.execute(s)
    conn.commit()
    
def exhaustCodesWithTime(time):
    '''use up codes that have the given initial time, ie set time left to 0'''
    s = 'UPDATE CODES_TABLE SET TIME = ? WHERE INITIAL_TIME=?'
    data_tuple = (0, time)
    conn.execute(s, data_tuple)
    conn.commit()
    
def checkCode(time_code):
    '''return -1 if code doesnt exist, return time left if code exists'''
    item = getRow(time_code)
    if item is None:
        print("No items")
        return -1
    else:
        time = item[TIME_LEFT_INDEX]
        return time
        
def dumpDB(file_name, mode=0):
    ''' mode=0 unused codes,
        mode=1 all codes,
        mode=2 unused codes,
    '''
    s = ''
    if mode == 0:
        s = '''SELECT * FROM CODES_TABLE WHERE (TIME!=0 AND TIME=INITIAL_TIME) 
            ORDER BY INITIAL_TIME ASC, TIME ASC'''
    elif mode == 1:
        s = 'SELECT * FROM CODES_TABLE ORDER BY INITIAL_TIME ASC, TIME ASC'
    elif mode == 2:
        s = '''SELECT * FROM CODES_TABLE WHERE (TIME!=0 AND TIME!=INITIAL_TIME) 
            ORDER BY INITIAL_TIME ASC, TIME ASC'''
    else: return
    cursor = conn.execute(s)
    with open(file_name, 'w') as f:
        f.write('\t Code : \t Time \t Time Left\n')
        prev_time = -1
        prices = {TEN: '15 bond\n',
                  FOURTEEN: '20 bond\n',
                  TWENTY: '30 bond\n',
                  THIRTY: '45 bond\n',
                  HOUR: '90 bond + bonus 10 minutes\n' }
        for item in cursor:
            time_left = (item[TIME_LEFT_INDEX]) // 60
            time = (item[INITIAL_TIME_INDEX] - 200) // 60
            if time != prev_time:
                #put newline separator when processing new time range
                f.write('\n')
                if item[INITIAL_TIME_INDEX] in prices:
                    f.write(prices[item[INITIAL_TIME_INDEX]])
                prev_time = time
            s = '\t {:>6d} \t {:} mins \t {:} mins\n'.format(item[0], time, time_left)
            f.write(s)
    

createTimeCodesTable()

