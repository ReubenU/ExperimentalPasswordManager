import os.path
import base64
import pickle
import pyperclip
import getpass
import passgenerate
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Main program storage for login editing and creation.
logins = {}

# Initial login to unlock the encrypted keyring.keys file.
masterpass = bytes(getpass.getpass('Unlock login ring with master password: '), 'utf-8')

# Derive key from master password
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'\xaab\xc0\xe0+\xc8\xb29\xc5\xe9\xbb\xfb\xaa\xb6\xab\xa7',
    iterations=100000,
    backend=default_backend()
)

# Derive the key and use it to create a Fernet encryption/decryption
# class.
key = base64.urlsafe_b64encode(kdf.derive(masterpass))

f = Fernet(key)


# Make a new login and generate a password
def genPassLogin(website, email, username):
    logins[website] = '{}:{}:{}'.format(
        email,
        username,
        passgenerate.newKey(
            int(time.strftime('%d%m%Y')
            )
        )
    )

def setGenPassLogin():
    print('Please enter login information in the following queries:\n')
    website = input('\tWebsite: ')
    email   = input('\tEmail: ')
    username= input('\tUsername: ')

    genPassLogin(website, email, username)

def newLogin():
    print('Please enter login information in the following format:\nwebsite email username password\n')

    website = input('\tWebsite: ')
    email   = input('\tEmail: ')
    username= input('\tUsername: ')
    password= input('\tPassword: ')

    logins[website] = '{}:{}:{}'.format(
        email,
        username,
        password
    )

# Delete the login information
# for a website.
def delLogin():
    website = input('Enter website of login to delete: ')
    logins.pop(website)


# Load and decrypt the logins and
# return them in string format.
def loadLogins():
    file = open('keyring.keys', 'rb')

    token = f.decrypt( pickle.load(file) )

    file.close()

    return token.decode('utf-8')


# Copy login password.
def copyPassword():
    website = input('Enter website: ')

    pyperclip.copy(logins[website].split(':')[2])

    print('Password copied.')


# Separate and load logins into the
# logins dictionary.
def parseLogins(strLogins):
    individual_logins = strLogins.split(';')

    for i in range(len(individual_logins)):
        if (individual_logins[i] != ''):

            website, email, username, password = individual_logins[i].split(':', 3)
                

            logins[website] = '{}:{}:{}'.format(
                email,
                username,
                password
            )


# Encrypt and save logins in a bytes file 
# using the master password.
def saveLogins():
    logs = ['{}'.format(x) for x in logins]
    pasw = ['{}'.format(logins[y]) for y in logins]

    keys = []

    for i in range(len(logins)):
        keys += logs[i] + ':' + pasw[i] + ';'

    print(''.join(keys))

    keyring = f.encrypt(bytes(''.join(keys), 'utf-8'))

    file = open('keyring.keys', 'wb')

    pickle.dump(keyring, file)

    file.close()


# Display all login information.
def showLogins():
    
    sorted_logins = dict(sorted(logins.items(), key=lambda kv: kv[0].lower()))
    
    for i in sorted_logins:
        info = sorted_logins[i].split(':')
        
        website = i
        email = info[0]
        username = info[1]
        password = info[2]
        
        print(f'\nWebsite:  {website}\nEmail:    {email}\nUsername: {username}\nPassword: {password}\n')
        

# Main function
def main():
    commands = {
        'newLogin' : [newLogin, ' - Create a new login.'],
        'updateLogin' : [newLogin, ' - Update an existing login.'],
        'genPassLogin' : [setGenPassLogin, ' - Set a login and autogenerate password.'],
        'deleteLogin' : [delLogin, ' - Delete a login.'],
        'saveLogins' : [saveLogins, ' - Save all logins to file.'],
        'showAll' : [showLogins, ' - Show all logins.'],
        'copyPassword' : [copyPassword,  '- Copy the password of the login you are about to select.'],
        'help' : [None, ' - show this list again.'],
        'quit' : [None, ' - Quit this application.']
    }

    if (os.path.exists('keyring.keys')):
        parseLogins(loadLogins())
        print('Logins loaded successfully!!!')
    
    #showLogins()
    
    print('Available commands: ')
    for command in commands:
        print('\t\t' + command + commands[command][1])

    while True:
        cmd = input('>>: ')

        if (cmd in commands):
            if (cmd == 'quit'):
                print('Quitting application...')

                return

            if (cmd == 'help'):
                print('Available commands: ')
                for command in commands:
                    print('\t\t' + command + commands[command][1])
                continue
            
            commands[cmd][0]()
            

    
if __name__ == '__main__':
    main()
