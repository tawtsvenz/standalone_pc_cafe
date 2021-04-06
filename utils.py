

import subprocess, ctypes, os
from random import randint
import win32gui, win32con

import tawsql
        
bonus_time = tawsql.bonus_time #seconds added to first ticket to allow for loading of games and setting up

def get_running_apps():
    #Get the running apps on the system and return the list of names
    results = list()
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description, Id, Path'
    proc = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if not line.decode()[0].isspace():
            print(line.decode().rstrip())
    
    
def minimise_running_app(handle_name):
    #mininise the app with the given names
    app_handle = ctypes.windll.user32.FindWindowW(None, handle_name)
    ctypes.windll.user32.ShowWindow(app_handle, 6)
    
def close_running_app(handle_name):
    #close the running app
    app_handle = ctypes.windll.user32.FindWindowW(None, handle_name)
    ctypes.windll.user32.CloseWindow(app_handle)
    
def minimise_foreground_app():
    app_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    minimise_running_app(app_name)
    
def close_foreground_app():
    app_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    #hack to prevent closing x360ce, just minimise_foreground_app
    if 'Jocys.com X360' in app_name:
        minimise_foreground_app()
        return
    app_handle = win32gui.FindWindow(None, app_name)
    win32gui.PostMessage(app_handle, win32con.WM_CLOSE, 0, 0)
    
def check_time_code(time_code):
    #checks if time code is valid.
    #returns 0 if code has been used already
    #returns -1 if code is invalid
    #returns time in seconds of the code
    try:
        time_code = int(time_code)
        return tawsql.checkCode(time_code)
    except Exception as e:
        print(e)
        return -1
        
def update_time_code(time_code, new_time, date_created=None, date_sold=None):
    #update the time code with new_time in seconds
    try:
        time_code = int(time_code)
        return tawsql.updateCode(time_code, new_time, date_created, date_sold)
    except Exception as e:
        print(e)
        return -1
        
def is_ticket_sold(time_code):
    return tawsql.isTicketSold(time_code)
    
def create_time_codes(seconds, quantity):
    #create time codes of the given quantity, each with the given seconds
    for x in range(quantity):
        code = randint(1000, 999999)
        tawsql.addCode(code, seconds)
        

debug = False
if debug == True:
    '''create_time_codes(600 + bonus_time, 30)
    create_time_codes(1200 + bonus_time, 30)
    create_time_codes(1800 + bonus_time, 30)
    create_time_codes(3600 + bonus_time, 30)'''
    #tawsql.deleteAllCodes()
    tawsql.dumpDB('dump.txt')
    pass
        
        

        