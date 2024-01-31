"""
    APiTalk
    Connected to SR API
"""
import requests
import xmltodict

API_URL = 'http://api.sr.se/api/v2'

def main():
    """
    Purpose: Program loop 
    """
    running = True
    while(running is True):
        print('\nSelect:')
        choice = input('(1)Show all channels.\n(2)Show all programms.\n(x)Quit\n')
        
        match choice:
            case '1':
                getchannels()
            case '2':
                getprograms()
            case 'x':
                print('Good bye!')
                break

def getchannels():
    """
    Purpose: Fetch all radiochannels.
    """
    r = requests.get(API_URL + '/channels', timeout=6)
    r.encoding = 'ISO-8859-1'
    chandict = xmltodict.parse(r.text)
    for v in chandict['sr']['channels']['channel']:
        print(f"{v['@name']}")

def getprograms():
    """
    Purpose: Fetch all radioprograms.
    """
    r = requests.get(API_URL + '/programs', timeout=6)
    r.encoding = 'ISO-8859-1'
    chandict = xmltodict.parse(r.text)
    for v in chandict['sr']['programs']['program']:
        print(f"{v['@name']}")

main()
