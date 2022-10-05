#imports the needed modules
import os, threading, getpass, difflib, platform, msvcrt
import audio.Audio_Func
import Credentials

#platform test
if platform.system() == 'Windows':
    pass
else:
    print('This program does not support %s operating systems. Press a space to quit.'%(platform.system()))
    msvcrt.getwch()
    
#start a threading event.
T = threading.Event()
#function to play the music passing the event object.
def Music():
    #starts the thread to run the function for the music with argument (needs to be iterable) with a die if the program ends.
    threading.Thread(target=audio.Audio_Func.BMusic, args=(T,), daemon=True).start()

#write the list of names to a file. Not going to add duplicates.
def Create_Append(NewNames):
    try:
        with open('Data\\VoterNames.txt', 'r+') as NameFile:
            Flist = NameFile.read().split(',')
            Noadd = set(Flist).intersection(NewNames)
            Flist.remove(Noadd) if (len(Noadd) > 0) else Flist
            if len(Noadd) > 0:
                print('There are a few names not added since they are duplicates.')
                #print(Noadd)
            ToAdd = set(NewNames).difference(set(Flist))
            if len(ToAdd) > 0:
                print('These are the names that will be added.')
                print(ToAdd)
                for N in ToAdd:
                    NameFile.write(N+',')
            else:
                print('No new names were added since no unique names were found.')
    except FileNotFoundError:
            with open('Data/VoterNames.txt', 'w') as NameFile:
                for Name in NewNames:
                    NameFile.write(Name+',')
            print('Because a list was not found, a new one was created.')
            #makes a password with an input passed.
            Credentials.NPwd(input('Please input a password to grant access to database.'))


#function to loop through asking user for Names.
def VoteNames():
    Music()
    vtrNms = []
    Cprint,Cpindex = 0,0
    print('Please enter names without special symbols or multiple spaces')
    print("Type 'end' to stop adding names, 'stop' to stop the music, or 'start' to restart the music")
    E = 0
    while True:#this is where the name are collected, then returned
        nms = input(': ')
        #we are test for posibilities of a space. Considered a special symbol which would be rejected when test alphanumeric.
        nms = nms.lower().title().strip()

        if ' ' in nms:
            tmp = nms.split(' ')
            for I in tmp:
                if I.isalnum() == False:
                    E+=1
                    nms = None
                
        elif nms.isalnum() == False:
            print('Names do not support special symbols.\nThis input will be rejected.')
            nms = None

        #testing for key words for specific actions.
        elif nms.lower() == 'end': 
            break
        elif nms.lower() == 'stop':
            T.set() #stops the music
            nms = None
            
        elif nms.lower() == 'start':
            T.clear()
            Music()
            nms = None


        if E > 0:
            print('Names do not support special symbols or multiple spaces.\nThis input will be rejected.')
            E = 0
        if nms != None:
            vtrNms.append(nms)
            if Cprint < 4:
                print(vtrNms[Cpindex:], end=' ')
                Cprint +=1
            else:
                print('='*42)
                print('[\''+vtrNms[-1]+'\']', end='')
                Cpindex = Cprint
                Cprint = 0
    
    #starts the music event to stop the music and adds the list info to the file by passing to another function.
    return T.set(),Create_Append(vtrNms)


#access the list from the file to read.
def AccessName():
    try:    
        with open('Data\\VoterNames.txt', 'r') as NameFileRead:
            RListName = NameFileRead.read().split(',')
            RListName.remove('')
            search = input('Type here to search for a name. ')
            RSearch = difflib.get_close_matches(search, RListName, 6)
            if RSearch == []:
                print('No \'good\' matching names were found')
            else:
                print('here is a list of potential names based on search.\n',RSearch)
                print('push any')
                msvcrt.getwch()
    #handling if file not found.
    except FileNotFoundError:
        CreatList = ''
        while True:
            CreatList = input('A list was not found.\nWould you like to make a new list anyway?(y/n) ')
            if CreatList.lower() == 'y':
                VoteNames()
                break
            elif CreatList.lower() == 'n':
                quit('The program has closed')
            else:
                print('Please type one of the expected answers.(y/n).')


#authentication
def Authentication():
    print('You are attempting to log in as  %s.'%(getpass.getuser()))
    Tries = 0
    while Tries != 3:
        #checks password by refering to credential functions check.
        if Credentials.Check(getpass.getpass(prompt='Password Please: ', stream=None)) == True:
            audio.Audio_Func.AccessGrant()
            AccessName()
            exit()
        else:
            audio.Audio_Func.FullStop()
            print('Password incorrect')
            Tries +=1
    exit('Login Failed')

#user option to access or add/create the list.
def UserOp():
    WhereToGo = ''
    while WhereToGo.lower() != 'access' or WhereToGo.lower() != 'create':
        WhereToGo = input('Would you like to access the list or create(append) to an existing list?\nType Create or access. or exit ')
        if WhereToGo.lower() == 'access':
            Authentication()
        elif WhereToGo.lower() == 'create':
            VoteNames()
            UserOp()
            break
        elif WhereToGo.lower() == 'exit':
            exit('The program was closed at the request of the user.')
        else:
            print('Please type an expected answer.')
UserOp()