key = "1234567890123456"
#The goal of this script is to decrypt files that have been encrypted by the ransomware.
#The script will take the key as an argument.

import os
import sys
import smtplib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend



#This function will decrypt the file using the key.
def decrypt(key, filename):
    chunksize = 64 * 1024
    #The output file will be the same as the input file, but without the .nile extension.
    outputFile = filename[:-5]

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
                outfile.truncate(filesize)

#This function will get the files from the OS
def getFiles():
    #This will get the files from the OS.
    files = os.listdir()
    #This will return the files.
    return files


#This function will decrypt the files.
def decryptFiles(key, files):
    #This will loop through the files.
    for file in files:
        #This will check if the file is encrypted.
        if file.endswith(".nile"):
            #This will decrypt the file.
            decrypt(key, file)
            #This will print the file name.
            print("Decrypted %s" % str(file))
        #This will check if the file is not encrypted.
        elif not file.endswith(".nile"):
            #This will print the file name.
            print("Not encrypted %s" % str(file))

def main():
    #This will get the files.
    files = getFiles()
    #This will get the key.
    #This will decrypt the files.
    decryptFiles(key, files)

#This will call the main function.
main()

