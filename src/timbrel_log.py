#!/usr/bin/python3


def info( argSender, argText1, argText2=None):
    newlineStart = '\n'
    newlineEnd=''
    if ( argSender != 'timbrel.py'):
        intend='    '
    else:
        intend=''    
    if isinstance(argText1, list):
       argText1.insert(0, argSender)
    if isinstance(argText1, str):
        argText1 = argSender + ': ' + argText1
    newlineEnd = '\n'
    if argText2!=None:
        print(newlineStart, intend,argText1,argText2, newlineEnd)
    else:
        print(newlineStart, intend,argText1, newlineEnd)
        
def error( argSender, argText1, argText2=None):
    if isinstance(argText1, list):
       argText1.insert(0, 'Error:')
    if isinstance(argText1, str):
        argText1 = 'Error: ' + argText1
    info( argSender, argText1, argText2)