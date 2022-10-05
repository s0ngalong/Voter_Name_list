import secrets, datetime, getpass
from hashlib import pbkdf2_hmac
#defin create password function.
def NPwd(Password:' str'):
    #create salt
    Flavor = secrets.token_bytes(128)
    #sha and random parameters to generate hex numbers.
    cryp = pbkdf2_hmac('sha3_512', Password.encode(), Flavor, 50001)
    Flavor,cryp =  Flavor.hex(),cryp.hex()
    #moving the salted hash around.
    storage = Flavor[0:8]+cryp[0:32]+Flavor[8:24]+cryp[32:64]+Flavor[24:56]+cryp[64:96]+Flavor[56:120]+cryp[96:129]+Flavor[120:256]
    #write to file.
    with open('Data\keys.txt', 'w') as key:
        key.write(storage)
    #logs for when changing passwords.
    try:
        with open('Data\\Logs.txt','a') as Logs:
            Logs.write(str(datetime.datetime.today())+'\n')
            Logs.write(getpass.getuser()+'changed password.\n')
    except FileNotFoundError:
        with open('Data\\Logs.txt', 'w') as Logs:
            Logs.write(str(datetime.datetime.today())+'\n')
            Logs.write(getpass.getuser()+'changed password.\n')
    return print('The password was created successfully.')

#check password
def Check(Password:'str'):
    #open file and read the hash.
    try:
        with open('Data\\keys.txt','r') as cPass:
            cPwd = cPass.read()
    except FileNotFoundError:
        exit('A password was not found. Please create a password to grant access.')
    if cPwd == '':
        exit('The password was tampered with.')
    #unscrambling the salt
    RFlavor = ''
    DelMove = {0:8,32:48,64:96,96:160,128:265}
    for Position1,Position2 in DelMove.items():
        RFlavor = RFlavor+cPwd[Position1:Position2]
        cPwd = cPwd.replace(cPwd[Position1:Position2], '')
    #recacluating with the user input password.
    CryptCheck = pbkdf2_hmac('sha3_512', Password.encode(), bytes.fromhex(RFlavor), 50001)
    #return True to pass and False if not matching.
    Grant = secrets.compare_digest(CryptCheck, bytes.fromhex(cPwd))
    s = ' Sucessfully Logged in' if Grant else ' Failed to Log in'
    try:
        with open('Data\\Logs.txt', 'a') as Logs:
            Logs.write('\n'+str(datetime.datetime.today())+'\n')
            Logs.write(getpass.getuser()+s+'\n')
    except FileNotFoundError:
        with open('Data\\Logs.txt', 'w') as Logs:
            Logs.write('\n'+str(datetime.datetime.today())+'\n')
            Logs.write(getpass.getuser()+s+'\n')
    #Grant will return a bolleon if password is correct it will return True if not it will return False.
    return Grant

